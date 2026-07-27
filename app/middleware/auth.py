# app/middleware/auth.py — Authentication Context Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.services.jwt import decode_token

class AuthMiddleware(BaseHTTPMiddleware):
    """
    Extracts Bearer JWT Access Token or session cookie and populates request.state.user.
    """
    async def dispatch(self, request, call_next):
        user_context = None
        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split("Bearer ")[1].strip()
            payload = decode_token(token)
            if payload:
                user_context = {
                    "id": payload.get("sub"),
                    "role": payload.get("role", "User")
                }

        if not user_context:
            access_cookie = request.cookies.get("dart_access_token")
            if access_cookie:
                payload = decode_token(access_cookie)
                if payload:
                    user_context = {
                        "id": payload.get("sub"),
                        "role": payload.get("role", "User")
                    }

        request.state.user = user_context or {"id": "guest_user", "role": "Guest"}
        response = await call_next(request)
        return response
