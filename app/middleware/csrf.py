# app/middleware/csrf.py — CSRF Token Protection Middleware
import secrets
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

CSRF_SECRET_COOKIE = "dart_csrf_token"

class CSRFMiddleware(BaseHTTPMiddleware):
    """
    Double-Submit Cookie CSRF Protection Middleware.
    Validates X-CSRF-Token header on POST, PUT, PATCH, DELETE requests.
    Exempts authorization/login endpoints if CSRF token is not yet established.
    """
    async def dispatch(self, request, call_next):
        method = request.method
        path = request.url.path

        # Generate new CSRF token if cookie is missing
        csrf_cookie = request.cookies.get(CSRF_SECRET_COOKIE)
        new_csrf_token = None
        if not csrf_cookie:
            new_csrf_token = secrets.token_hex(20)
            csrf_cookie = new_csrf_token

        # Enforce validation on mutating requests
        if method in ["POST", "PUT", "PATCH", "DELETE"]:
            # Exempt auth signup/login/google endpoints
            if not path.startswith("/api/auth/"):
                header_token = request.headers.get("X-CSRF-Token")
                if not header_token or header_token != csrf_cookie:
                    return JSONResponse(
                        {"error": "CSRF Validation Failed", "detail": "Invalid or missing X-CSRF-Token header"},
                        status_code=403
                    )

        response: Response = await call_next(request)
        token_to_set = new_csrf_token or csrf_cookie
        if token_to_set:
            response.set_cookie(
                key=CSRF_SECRET_COOKIE,
                value=token_to_set,
                httponly=False,  # Client JS reads cookie to send in X-CSRF-Token header
                samesite="lax",
                secure=False,
                path="/"
            )
        return response
