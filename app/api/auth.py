# app/api/auth.py — Production Authentication API Router
import uuid, time
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Response, Request
from pydantic import BaseModel, EmailStr
from typing import Optional

from app.api.db import get_db
from app.services.passwords import hash_password, verify_password, validate_password_strength
from app.services.jwt import create_access_token, create_refresh_token, decode_token, revoke_refresh_token
from app.services.oauth import verify_google_token
from app.services.email import create_verification_token, verify_email_token, create_password_reset_token, verify_password_reset_token

router = APIRouter()

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class GoogleAuthRequest(BaseModel):
    credential: str

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

@router.post("/auth/signup")
def signup(body: SignupRequest, response: Response):
    valid, msg = validate_password_strength(body.password)
    if not valid:
        raise HTTPException(status_code=400, detail=msg)

    email = body.email.strip().lower()
    now = datetime.now(timezone.utc).isoformat()
    uid = str(uuid.uuid4())
    pw_hash = hash_password(body.password)

    with get_db() as conn:
        cursor = conn.cursor()
        existing = cursor.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="User with this email already exists")

        cursor.execute(
            """INSERT INTO users (id, uuid, name, email, password_hash, role, email_verified, created_at, updated_at, status)
               VALUES (?, ?, ?, ?, ?, 'User', 0, ?, ?, 'active')""",
            (uid, uid, body.name, email, pw_hash, now, now)
        )
        conn.commit()

    access_token = create_access_token(uid, "User")
    refresh_token = create_refresh_token(uid)

    response.set_cookie(key="dart_access_token", value=access_token, httponly=True, samesite="lax")
    response.set_cookie(key="dart_refresh_token", value=refresh_token, httponly=True, samesite="lax")

    return {"status": "success", "user": {"id": uid, "name": body.name, "email": email, "role": "User"}, "access_token": access_token}

@router.post("/auth/login")
def login(body: LoginRequest, response: Response):
    email = body.email.strip().lower()
    with get_db() as conn:
        cursor = conn.cursor()
        user = cursor.execute("SELECT id, name, email, password_hash, role, failed_attempts, locked_until FROM users WHERE email = ?", (email,)).fetchone()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        uid, name, uemail, pw_hash, role, failed_attempts, locked_until = user

        if not verify_password(body.password, pw_hash or ""):
            cursor.execute("UPDATE users SET failed_attempts = failed_attempts + 1 WHERE id = ?", (uid,))
            conn.commit()
            raise HTTPException(status_code=401, detail="Invalid email or password")

        cursor.execute("UPDATE users SET failed_attempts = 0, last_login = ?, login_count = login_count + 1 WHERE id = ?", (datetime.now(timezone.utc).isoformat(), uid))
        conn.commit()

    access_token = create_access_token(uid, role)
    refresh_token = create_refresh_token(uid)

    response.set_cookie(key="dart_access_token", value=access_token, httponly=True, samesite="lax")
    response.set_cookie(key="dart_refresh_token", value=refresh_token, httponly=True, samesite="lax")

    return {"status": "success", "user": {"id": uid, "name": name, "email": uemail, "role": role}, "access_token": access_token}

@router.post("/auth/google")
def google_auth(body: GoogleAuthRequest, response: Response):
    info = verify_google_token(body.credential)
    email = info["email"]
    now = datetime.now(timezone.utc).isoformat()

    with get_db() as conn:
        cursor = conn.cursor()
        user = cursor.execute("SELECT id, name, email, role FROM users WHERE email = ?", (email,)).fetchone()
        if user:
            uid, name, uemail, role = user
        else:
            uid = str(uuid.uuid4())
            name = info["name"]
            role = "User"
            cursor.execute(
                """INSERT INTO users (id, uuid, name, email, google_id, avatar, role, email_verified, created_at, updated_at, status)
                   VALUES (?, ?, ?, ?, ?, ?, 'User', 1, ?, ?, 'active')""",
                (uid, uid, name, email, info["google_id"], info["avatar"], now, now)
            )
            conn.commit()

    access_token = create_access_token(uid, role)
    refresh_token = create_refresh_token(uid)

    response.set_cookie(key="dart_access_token", value=access_token, httponly=True, samesite="lax")
    response.set_cookie(key="dart_refresh_token", value=refresh_token, httponly=True, samesite="lax")

    return {"status": "success", "user": {"id": uid, "name": name, "email": email, "role": role}, "access_token": access_token}

@router.post("/auth/logout")
def logout(response: Response):
    response.delete_cookie("dart_access_token")
    response.delete_cookie("dart_refresh_token")
    return {"status": "logged_out"}
