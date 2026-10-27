import cv2
from ultralytics import YOLO

model = YOLO("costume_yolo11n.pt")

# webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # run YOLO inference
    results = model(frame)

    annotated_frame = results[0].plot()

    cv2.imshow("YOLO Live Feed", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()