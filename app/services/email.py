# app/services/email.py — Email Verification & Password Reset Token Dispatcher
import secrets, time
from typing import Dict, Any

VERIFICATION_TOKENS: Dict[str, Dict[str, Any]] = {}
RESET_TOKENS: Dict[str, Dict[str, Any]] = {}

def create_verification_token(user_id: str) -> str:
    token = f"ver_{secrets.token_hex(20)}"
    VERIFICATION_TOKENS[token] = {
        "user_id": user_id,
        "expires_at": time.time() + 86400  # 24 hours
    }
    return token

def verify_email_token(token: str) -> tuple[bool, str]:
    if token not in VERIFICATION_TOKENS:
        return False, "Invalid or expired verification token"
    info = VERIFICATION_TOKENS[token]
    if time.time() > info["expires_at"]:
        del VERIFICATION_TOKENS[token]
        return False, "Verification token has expired"
    user_id = info["user_id"]
    del VERIFICATION_TOKENS[token]
    return True, user_id

def create_password_reset_token(user_id: str) -> str:
    token = f"rst_{secrets.token_hex(20)}"
    RESET_TOKENS[token] = {
        "user_id": user_id,
        "expires_at": time.time() + 1800  # 30 minutes
    }
    return token

def verify_password_reset_token(token: str) -> tuple[bool, str]:
    if token not in RESET_TOKENS:
        return False, "Invalid or expired password reset token"
    info = RESET_TOKENS[token]
    if time.time() > info["expires_at"]:
        del RESET_TOKENS[token]
        return False, "Password reset link has expired"
    user_id = info["user_id"]
    del RESET_TOKENS[token]
    return True, user_id
