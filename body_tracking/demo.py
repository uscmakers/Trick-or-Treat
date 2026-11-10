import cv2
from ultralytics import YOLO

model = YOLO("costume_yolo11n.pt")

# webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# buffer
MAX_MISSING_FRAMES = 15

# track people IDs
tracked_ids = set()
missing_counter = {}

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # run YOLO inference
    results = model.track(
        source=frame,
        persist=True,
        classes=[0],
        tracker='bytetrack.yaml',
        verbose=False
    )
    annotated_frame = results[0].plot()

    curr_ids = set()
    if results[0].boxes.id is not None:
        curr_ids = set(results[0].boxes.id.int().tolist())

    for id in curr_ids:
        # if id was missing but returned, reset missing counter
        if id in missing_counter:
            del missing_counter[id]

        # if id is completely new, register as ENTRY
        if id not in tracked_ids:
            tracked_ids.add(id)
            print(f'ENTERED {id}')

    # figure out which ids are not currently in frame anymore
    lost_ids = tracked_ids - curr_ids
    for id in lost_ids:
        missing_counter[id] = missing_counter.get(id, 0) + 1

        # if missing for longer than buffer, EXIT
        if missing_counter[id] > MAX_MISSING_FRAMES:
            tracked_ids.remove(id)
            del missing_counter[id]
            print(f'EXITED {id}') 

    # counter UI
    count = len(tracked_ids) # includes ids that are not currently in frame but within the buffer

    cv2.rectangle(annotated_frame, (10, 10), (250, 50), (0, 0, 0), -1)
    cv2.putText(
        annotated_frame, 
        f"People in Frame: {count}", 
        (20, 38), 
        cv2.FONT_HERSHEY_SIMPLEX, 
        0.7, 
        (0, 255, 0), 
        2
    )

    cv2.imshow("YOLO Live Feed", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()