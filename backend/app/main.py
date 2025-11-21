from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from fastapi.concurrency import run_in_threadpool
from pathlib import Path
from backend.app.tts_murf import tts_generate  # your tts function

app = FastAPI()

# Allow frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent.parent / "frontend"
STATIC_AUDIO_DIR = BASE_DIR / "static/audio"
STATIC_AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# Serve frontend static files
app.mount("/static", StaticFiles(directory=FRONTEND_DIR / "static"), name="static")
app.mount("/audio", StaticFiles(directory=STATIC_AUDIO_DIR), name="audio")

@app.get("/")
async def serve_frontend():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.post("/speak")
async def speak_endpoint(request: Request):
    try:
        body = await request.json()
        text = body.get("text", "").strip()
    except Exception:
        raw = await request.body()
        text = raw.decode("utf-8").strip()

    if not text:
        return JSONResponse({"error": "No message received"}, status_code=400)

    try:
        filename = await run_in_threadpool(tts_generate, text)
        return JSONResponse({
            "message": "Speech generated",
            "audio_url": f"/audio/{filename}"
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
