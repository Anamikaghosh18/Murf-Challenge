import requests
import uuid
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("MURF_API_KEY")

AUDIO_OUTPUT_DIR = Path(__file__).resolve().parent / "static/audio"
AUDIO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def tts_generate(text: str) -> str:
    """Generate speech using Murf REST API and return the filename."""
    filename = f"{uuid.uuid4()}.mp3"
    file_path = AUDIO_OUTPUT_DIR / filename

    url = "https://global.api.murf.ai/v1/speech/stream"
    headers = {
        "api-key": API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "voice_id": "en-US-alicia",  
        "text": text,
        "multi_native_locale": "en-US",
        "model": "FALCON",
        "format": "MP3",
        "sampleRate": 24000,
        "channelType": "MONO"
    }

    response = requests.post(url, headers=headers, json=data, stream=True)

    if response.status_code == 200:
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return filename
    else:
        raise Exception(f"Murf TTS failed: {response.status_code} {response.text}")
