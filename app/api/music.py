# app/api/music.py — AI Music Studio router
import requests, json, time, os, random, string, re, uuid, threading
from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

router = APIRouter()

MUSIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static", "music")
os.makedirs(MUSIC_DIR, exist_ok=True)

_jobs: dict = {}

_HEADERS = {
    "accept":          "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type":    "application/json",
    "origin":          "https://crevid.ai",
    "referer":         "https://crevid.ai/",
    "user-agent":      "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36",
}

def _make_email():
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    r = requests.post(
        "https://api.internal.temp-mail.io/api/v3/email/new",
        json={"min_name_length": 10, "max_name_length": 10, "name": name, "domain": "bwmyga.com"},
        timeout=15,
    )
    return r.json()

def _get_mail(addr):
    try:
        r = requests.get(f"https://api.internal.temp-mail.io/api/v3/email/{addr}/messages", timeout=10)
        msgs = r.json()
        return msgs[0] if msgs else None
    except:
        return None

def _clean_name(title: str) -> str:
    title = re.sub(r'[\\/*?:"<>|]', '', title)
    title = re.sub(r'[\s_]+', '-', title)
    title = re.sub(r'-+', '-', title)
    return title.strip('-')

def _download_file(sess, url, path):
    if not url.startswith("http"):
        url = "https://tomodel.crevid.ai/" + url.lstrip("/")
    try:
        r = sess.get(url, headers=_HEADERS, stream=True, timeout=60)
        if r.status_code == 200:
            with open(path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return True
    except:
        pass
    return False

def _generate(job_id: str, prompt: str):
    job = _jobs[job_id]

    def log(msg): job["log"].append(msg)

    try:
        log("📧 Creating temporary email...")
        mail_data = _make_email()
        email = mail_data.get("email")
        if not email:
            job["status"] = "error"; log("❌ Failed to create email"); return

        sess = requests.Session()
        sess.headers.update(_HEADERS)

        log("🔗 Requesting magic link sign-in...")
        r = sess.post(
            "https://crevid.ai/api/auth/sign-in/magic-link",
            json={"email": email, "name": email, "callbackURL": "/"},
            timeout=15,
        )
        if r.status_code != 200:
            job["status"] = "error"; log(f"❌ Sign-in failed ({r.status_code})"); return

        log("⏳ Waiting for magic link email...")
        magic_url = None
        for _ in range(30):
            msg = _get_mail(email)
            if msg:
                body = msg.get("body_html", "") or msg.get("body_text", "")
                m = re.search(r'(https://crevid\.ai/api/auth/magic-link/verify\?token=[^"&]+&callbackURL=%2F)', body)
                if m:
                    magic_url = m.group(1)
                    break
            time.sleep(2)

        if not magic_url:
            job["status"] = "error"; log("❌ Magic link not received"); return

        log("✅ Verifying magic link...")
        r = sess.get(magic_url, timeout=15)
        if r.status_code not in (200, 302):
            job["status"] = "error"; log("❌ Magic link verification failed"); return

        log("🎵 Sending music generation request...")
        r = sess.post(
            "https://crevid.ai/api/p1_generate/suno",
            json={"model": "V4", "prompt": prompt, "instrumental": False, "customMode": False, "title": "", "style": ""},
            timeout=30,
        )
        resp = r.json()
        task_id = resp.get("taskId")
        creation_id = resp.get("id")
        if not task_id:
            job["status"] = "error"; log("❌ Generation task not started"); return

        log("⏳ Generating music (this takes 2–4 minutes)...")
        for _ in range(120):
            time.sleep(3)
            r = sess.get(f"https://crevid.ai/api/p1_callbacks/suno?taskId={task_id}", timeout=15)
            info = r.json()
            if info.get("success") is True or (info.get("processing") is False and info.get("success") is False):
                break

        time.sleep(5)

        log("📦 Fetching generated files...")
        r = sess.get(f"https://crevid.ai/api/creation?id={creation_id}", timeout=15)
        creation = r.json()
        if "creation" not in creation:
            job["status"] = "error"; log("❌ Could not fetch creation data"); return

        meta    = json.loads(creation["creation"]["metadata"])
        songs   = meta.get("sunoData", [])
        if not songs:
            job["status"] = "error"; log("❌ No songs in response"); return

        song   = songs[0]
        title  = song.get("title", "Track") or "Track"
        safe   = _clean_name(title)
        mp3_path = os.path.join(MUSIC_DIR, f"{job_id}.mp3")
        jpg_path = os.path.join(MUSIC_DIR, f"{job_id}.jpg")
        lyrics   = (song.get("prompt") or song.get("lyric") or song.get("lyrics") or
                    meta.get("lyric", ""))

        if song.get("audioUrl"):
            log("⬇️ Downloading MP3...")
            _download_file(sess, song["audioUrl"], mp3_path)
        if song.get("imageUrl"):
            log("🖼️ Downloading cover art...")
            _download_file(sess, song["imageUrl"], jpg_path)

        job["title"]  = title
        job["lyrics"] = lyrics
        job["mp3"]    = f"/api/music/file/{job_id}.mp3" if os.path.exists(mp3_path) else None
        job["cover"]  = f"/api/music/file/{job_id}.jpg" if os.path.exists(jpg_path) else None
        job["status"] = "done"
        log("✅ Done!")

    except Exception as e:
        job["status"] = "error"
        job["log"].append(f"❌ Error: {str(e)}")

class MusicRequest(BaseModel):
    prompt: str

@router.post("/music")
def start_music(body: MusicRequest):
    job_id = str(uuid.uuid4())[:8]
    _jobs[job_id] = {"status": "running", "log": [], "title": None, "lyrics": None, "mp3": None, "cover": None}
    threading.Thread(target=_generate, args=(job_id, body.prompt), daemon=True).start()
    return {"job_id": job_id}

@router.get("/music/{job_id}")
def get_music_status(job_id: str):
    job = _jobs.get(job_id)
    if not job:
        return JSONResponse({"error": "Job not found"}, status_code=404)
    return job

@router.get("/music/file/{filename}")
def serve_music_file(filename: str):
    path = os.path.join(MUSIC_DIR, filename)
    if not os.path.exists(path):
        return JSONResponse({"error": "File not found"}, status_code=404)
    media = "audio/mpeg" if filename.endswith(".mp3") else "image/jpeg"
    return FileResponse(path, media_type=media)
