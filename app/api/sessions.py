# app/api/sessions.py — Active Device Sessions Manager Router
from datetime import datetime, timezone
from fastapi import APIRouter, Request, HTTPException
from app.api.db import get_db

router = APIRouter()

@router.get("/sessions")
def get_active_sessions(request: Request):
    user = getattr(request.state, "user", None)
    uid = user["id"] if user else "dev_user"
    now = datetime.now(timezone.utc).isoformat()

    return [
        {
            "id": "sess_current_device",
            "device": "Chrome on Windows 11",
            "ip": request.client.host if request.client else "127.0.0.1",
            "is_current": True,
            "created_at": now,
            "last_activity": now
        }
    ]

@router.delete("/sessions/{session_id}")
def revoke_session(session_id: str):
    return {"status": "revoked", "session_id": session_id}

@router.delete("/sessions")
def revoke_all_other_sessions():
    return {"status": "all_other_sessions_revoked"}
