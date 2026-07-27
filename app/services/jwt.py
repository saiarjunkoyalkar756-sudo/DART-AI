# app/services/jwt.py — JWT Access & Refresh Token Manager
import time, secrets, json, base64, hashlib
from typing import Optional, Dict, Any

SECRET_KEY = "dart_ai_production_jwt_secret_key_2026"
ACCESS_TOKEN_EXPIRE_SECONDS = 900  # 15 minutes
REFRESH_TOKEN_EXPIRE_SECONDS = 604800  # 7 days

REVOKED_TOKENS = set()

def _base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def _base64url_decode(data: str) -> bytes:
    padding = '=' * (4 - (len(data) % 4))
    return base64.urlsafe_b64decode(data + padding)

def create_access_token(user_id: str, role: str = "User") -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": user_id,
        "role": role,
        "iat": int(time.time()),
        "exp": int(time.time()) + ACCESS_TOKEN_EXPIRE_SECONDS,
        "jti": secrets.token_hex(8)
    }
    encoded_header = _base64url_encode(json.dumps(header).encode('utf-8'))
    encoded_payload = _base64url_encode(json.dumps(payload).encode('utf-8'))
    signature_input = f"{encoded_header}.{encoded_payload}".encode('utf-8')
    signature = hashlib.sha256(signature_input + SECRET_KEY.encode('utf-8')).hexdigest()
    return f"{encoded_header}.{encoded_payload}.{signature}"

def create_refresh_token(user_id: str) -> str:
    token = f"ref_{user_id}_{secrets.token_hex(24)}"
    return token

def decode_token(token: str) -> Optional[Dict[str, Any]]:
    if not token or token in REVOKED_TOKENS:
        return None
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        encoded_header, encoded_payload, signature = parts
        signature_input = f"{encoded_header}.{encoded_payload}".encode('utf-8')
        expected_sig = hashlib.sha256(signature_input + SECRET_KEY.encode('utf-8')).hexdigest()
        if not secrets.compare_digest(signature, expected_sig):
            return None
        payload = json.loads(_base64url_decode(encoded_payload).decode('utf-8'))
        if payload.get("exp", 0) < time.time():
            return None
        return payload
    except:
        return None

def revoke_refresh_token(token: str):
    REVOKED_TOKENS.add(token)
