
import requests

url = "https://global.api.murf.ai/v1/speech/stream"
headers = {
    "api-key": "MURF_API_KEY",
    "Content-Type": "application/json"
}
data = {
   "voice_id": "en-US-matthew",
   "text": "Hello! How can I assist you today? Please let me know your issue, and I'll do my best to help.",
   "multi_native_locale": "en-US",
   "model": "FALCON",
   "format": "MP3",
   "sampleRate": 24000,
   "channelType": "MONO"
}

response = requests.post(url, headers=headers, json=data, stream=True)

if response.status_code == 200:
    with open("audio.mp3", "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                # Process chunks in real-time if needed
                print(f"Received {len(chunk)} bytes")
    print("Audio streaming completed")
else:
    print(f"Error: {response.status_code}")
