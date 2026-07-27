# app/api/mail.py — Temporary Email Service router
import re
import requests, sqlite3, os, secrets, string, base64, gzip
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

BASE  = "https://dark.ps"
DOMAIN = "dark.ps"
CHARS  = string.ascii_lowercase + string.digits
DB_PATH = os.path.expanduser("~/.darkai_mail.db")

def _key():
    h = hash(DB_PATH + "dark")
    return bytes([h % 256, (h >> 8) % 256, (h >> 16) % 256, (h >> 24) % 256])

def _enc(data: str) -> str:
    k = _key()
    x = bytes([b ^ k[i % len(k)] for i, b in enumerate(data.encode())])
    return base64.b64encode(gzip.compress(x)).decode()

def _dec(enc: str) -> str:
    k = _key()
    x = gzip.decompress(base64.b64decode(enc))
    return ''.join(chr(b ^ k[i % len(k)]) for i, b in enumerate(x))

def _init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("CREATE TABLE mails(id TEXT PRIMARY KEY, email TEXT, created TEXT, encrypted TEXT)")
        conn.commit()
        conn.close()

def _list_mails():
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, email, created, encrypted FROM mails ORDER BY created DESC")
    rows = []
    for row in c.fetchall():
        try:
            raw = _dec(row[3])
        except:
            raw = "?"
        rows.append({"id": row[0], "email": row[1], "created": row[2], "raw": raw})
    conn.close()
    return rows

def _save_mail(email: str):
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    mid = ''.join(secrets.choice(CHARS) for _ in range(8))
    enc = _enc(email)
    conn.execute(
        "INSERT OR REPLACE INTO mails VALUES(?,?,?,?)",
        (mid, email, datetime.now(timezone.utc).isoformat(), enc)
    )
    conn.commit()
    conn.close()
    return mid

def _delete_mail(mail_id: str):
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM mails WHERE id=?", (mail_id,))
    conn.commit()
    conn.close()

def _expires_secs(created: str) -> int:
    dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
    expire_at = dt + timedelta(seconds=7200)
    remaining = expire_at - datetime.now(timezone.utc)
    return max(0, int(remaining.total_seconds()))

def _api(path: str, data=None):
    try:
        if data:
            r = requests.post(f"{BASE}{path}", json=data, timeout=20)
        else:
            r = requests.get(f"{BASE}{path}", timeout=20)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"ok": False, "err": str(e)}

def _rand_local(n=10):
    return ''.join(secrets.choice(CHARS) for _ in range(n))

class NewMailRequest(BaseModel):
    prefix: Optional[str] = None

@router.post("/mail/new")
def new_mail(body: NewMailRequest = None):
    prefix = (body.prefix if body and body.prefix else "").strip()
    if not prefix:
        prefix = _rand_local()

    email = f"{prefix}@{DOMAIN}"
    res = _api(f"/api/v1/mail/email?address={email}")
    mid = _save_mail(email)

    return {
        "id":            mid,
        "email":         email,
        "expires_in":    7200,
        "api_response":  res,
    }

@router.get("/mail/generate")
def generate_mail():
    prefix = _rand_local()
    email  = f"{prefix}@{DOMAIN}"
    mid    = _save_mail(email)
    return {"id": mid, "email": email, "expires_in": 7200}

@router.get("/mail/list")
def list_saved_mails():
    mails = _list_mails()
    for m in mails:
        m["expires_in"] = _expires_secs(m["created"])
    return mails

@router.get("/mail/inbox")
def get_inbox(email: str):
    return _api(f"/api/v1/mail/inbox?address={email}")

@router.delete("/mail/{mail_id}")
def delete_saved_mail(mail_id: str, email: Optional[str] = None):
    _delete_mail(mail_id)
    if email:
        _api(f"/api/v1/mail/email?address={email}")
    return {"ok": True}
