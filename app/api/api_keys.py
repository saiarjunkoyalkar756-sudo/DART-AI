# app/api/api_keys.py — Scoped API Keys Management Router
import uuid, secrets, hashlib
from datetime import datetime, timezone
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.api.db import get_db

router = APIRouter()

class CreateApiKeyRequest(BaseModel):
    name: str = "Production API Key"
    scopes: List[str] = ["chat", "image", "music", "search"]

@router.get("/api-keys")
def get_user_api_keys(request: Request):
    user = getattr(request.state, "user", None)
    uid = user["id"] if user else "dev_user"
    with get_db() as conn:
        cursor = conn.cursor()
        rows = cursor.execute("SELECT id, key_name, key_prefix, scopes, created_at, last_used FROM api_keys WHERE user_id = ?", (uid,)).fetchall()
        if not rows:
            now = datetime.now(timezone.utc).isoformat()
            return [{
                "id": "key_demo",
                "name": "Default Developer Key",
                "prefix": "dart_sk_live_demo",
                "scopes": ["chat", "image", "music", "search"],
                "created_at": now,
                "last_used": now
            }]
        return [
            {
                "id": r[0],
                "name": r[1],
                "prefix": r[2],
                "scopes": r[3].split(",") if r[3] else [],
                "created_at": r[4],
                "last_used": r[5]
            }
            for r in rows
        ]

@router.post("/api-keys")
def create_api_key(body: CreateApiKeyRequest, request: Request):
    user = getattr(request.state, "user", None)
    uid = user["id"] if user else "dev_user"
    kid = str(uuid.uuid4())
    raw_secret = f"dart_sk_live_{secrets.token_hex(16)}"
    prefix = raw_secret[:16]
    secret_hash = hashlib.sha256(raw_secret.encode('utf-8')).hexdigest()
    scopes_str = ",".join(body.scopes)
    now = datetime.now(timezone.utc).isoformat()

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO api_keys (id, user_id, key_name, secret_hash, key_prefix, scopes, created_at, last_used)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (kid, uid, body.name, secret_hash, prefix, scopes_str, now, now)
        )
        conn.commit()

    return {
        "id": kid,
        "name": body.name,
        "api_key": raw_secret,
        "prefix": prefix,
        "scopes": body.scopes,
        "created_at": now
    }

@router.delete("/api-keys/{key_id}")
def revoke_api_key(key_id: str, request: Request):
    user = getattr(request.state, "user", None)
    uid = user["id"] if user else "dev_user"
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM api_keys WHERE id = ? AND user_id = ?", (key_id, uid))
        conn.commit()
    return {"status": "revoked", "key_id": key_id}
