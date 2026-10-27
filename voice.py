
import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play

load_dotenv()

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

def speak(text):
    audio = client.text_to_speech.convert(
        text=text,
        voice_id=VOICE_ID,
        model_id="eleven_v3",
        output_format="mp3_44100_128",
    )
    play(audio)
