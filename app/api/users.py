# app/api/users.py — User Profile & Account Management API Router
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
from app.api.db import get_db
from app.services.passwords import hash_password, verify_password, validate_password_strength

router = APIRouter()

class ProfileUpdateRequest(BaseModel):
    name: str

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

@router.get("/users/me")
def get_current_user_profile(request: Request):
    user = getattr(request.state, "user", None)
    uid = user["id"] if user else "dev_user"
    with get_db() as conn:
        cursor = conn.cursor()
        row = cursor.execute("SELECT id, name, email, avatar, role, email_verified, two_factor_enabled, created_at FROM users WHERE id = ?", (uid,)).fetchone()
        if row:
            return {"id": row[0], "name": row[1], "email": row[2], "avatar": row[3], "role": row[4], "email_verified": bool(row[5]), "two_factor_enabled": bool(row[6]), "created_at": row[7]}
        return {"id": uid, "name": "Dev User", "email": "dev.user@gmail.com", "avatar": "", "role": "User", "email_verified": True, "two_factor_enabled": False}

@router.put("/users/me")
def update_profile(body: ProfileUpdateRequest, request: Request):
    user = getattr(request.state, "user", None)
    uid = user["id"] if user else "dev_user"
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET name = ? WHERE id = ?", (body.name, uid))
        conn.commit()
    return {"status": "updated", "name": body.name}

@router.post("/users/change-password")
def change_password(body: ChangePasswordRequest, request: Request):
    user = getattr(request.state, "user", None)
    uid = user["id"] if user else "dev_user"
    valid, msg = validate_password_strength(body.new_password)
    if not valid:
        raise HTTPException(status_code=400, detail=msg)

    with get_db() as conn:
        cursor = conn.cursor()
        row = cursor.execute("SELECT password_hash FROM users WHERE id = ?", (uid,)).fetchone()
        if row and row[0]:
            if not verify_password(body.current_password, row[0]):
                raise HTTPException(status_code=400, detail="Current password incorrect")
        new_hash = hash_password(body.new_password)
        cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, uid))
        conn.commit()
    return {"status": "password_changed"}
