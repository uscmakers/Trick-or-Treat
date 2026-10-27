
from kokoro import KPipeline
import sounddevice as sd

pipeline = KPipeline(lang_code="a")

voices = [
    "am_adam",
    "am_michael",
    "am_echo",
    "am_eric",
    "am_fenrir",
    "am_onyx",
    "am_puck",
]

# Different lines to test dramatic delivery
lines = [
    "Well, well, well... Another visitor. How unfortunate.",
    "And I wanted a neck... Life is full of disappointments.",
    "Oh, you're not afraid of me? How... interesting.",
    "Go on. Reach inside my head. I dare you.",
]

speeds = [0.9, 1.0, 1.1]

def speak_sample(text, voice, speed):
    for _, _, audio in pipeline(
        text,
        voice=voice,
        speed=speed
    ):
        sd.play(audio, samplerate=24000)
        sd.wait()

for voice in voices:
    print(f"\n{'=' * 45}")
    print(f"VOICE: {voice}")
    print(f"{'=' * 45}")

    for speed in speeds:
        print(f"\nSpeed: {speed}x")

        for line in lines:
            print(f"  {line}")
            speak_sample(line, voice, speed)

        input("\nPress Enter to try the next speed...")

    input(f"\nFinished {voice}. Press Enter for next voice...")

print("\nAll voices tested!")
