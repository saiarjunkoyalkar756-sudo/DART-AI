# app/api/tts.py — Text-to-Speech router
import requests, uuid, datetime, random
from fastapi import APIRouter
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel

router = APIRouter()

VOICES = ["coral", "alloy", "echo", "fable", "nova", "onyx", "shimmer"]

_tts_state = {
    "token":     None,
    "device_id": ''.join(random.choices('0123456789abcdef', k=16)),
    "session_id": str(uuid.uuid4()) + "R",
    "msg_count": 0,
}

def _auth() -> bool:
    s = _tts_state
    try:
        r = requests.post(
            "https://api.chatboxapp.ai/auth/v2/users",
            headers={
                "user-agent":    "ChatBox/1.82.3 (Windows_NT 10.0.19045; x64)",
                "content-type":  "application/json",
                "accept":        "application/json",
                "accept-encoding": "gzip, deflate, br",
                "connection":    "keep-alive",
            },
            params={"deviceId": s["device_id"], "appName": "ChatBox"},
            json={"strategy": "windowsV1"},
            timeout=15,
        )
        if r.status_code == 201:
            s["token"]     = r.json().get("accessToken")
            s["msg_count"] = 0
            return True
        return False
    except:
        return False

def stream_tts(text: str, voice: str = "coral", instructions: str = ""):
    s = _tts_state

    if not s["token"] or s["msg_count"] >= 3:
        if not _auth():
            yield b""
            return

    inst = instructions.strip() or (
        "Speak in a warm, natural, and expressive voice. Be conversational and clear, "
        "with a friendly tone similar to a helpful assistant. Use natural pacing."
    )

    headers = {
        "authority":          "api.florate.io",
        "accept":             "audio/mpeg, application/json",
        "authorization":      f"Bearer {s['token']}",
        "content-type":       "application/json",
        "origin":             "https://app.chatbox.ai",
        "referer":            "https://app.chatbox.ai/",
        "user-agent":         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/132.0.0.0 Safari/537.36",
        "accept-language":    "en-US,en;q=0.9",
        "x-date":             datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT"),
    }

    try:
        r = requests.post(
            "https://api.florate.io/text-to-speech",
            headers=headers,
            json={"model": "gpt-4o-mini-tts", "prompt": text, "voice": voice, "instructions": inst},
            stream=True,
            timeout=(15, 120),
        )

        if r.status_code != 200:
            return

        for chunk in r.iter_content(chunk_size=4096):
            if chunk:
                yield chunk

        s["msg_count"] += 1

    except:
        return

class TtsRequest(BaseModel):
    text:         str
    voice:        str = "coral"
    instructions: str = ""

@router.get("/tts/voices")
def get_voices():
    return VOICES

@router.post("/tts/generate")
def generate_tts(body: TtsRequest):
    voice = body.voice if body.voice in VOICES else "coral"
    return StreamingResponse(
        stream_tts(body.text, voice, body.instructions),
        media_type="audio/mpeg",
        headers={"Content-Disposition": f"attachment; filename=speech_{voice}.mp3"},
    )
