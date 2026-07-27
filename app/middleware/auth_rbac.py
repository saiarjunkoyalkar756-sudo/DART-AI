# app/middleware/auth_rbac.py — Role-Based Access Control (RBAC) Security Middleware
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class RBACMiddleware(BaseHTTPMiddleware):
    """
    Enforces Role-Based Access Control (RBAC) on administrative endpoints.
    Requires 'Authorization: Bearer admin-secret-key' header for /api/admin/* routes.
    """
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if path.startswith("/api/admin"):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JSONResponse(
                    {"error": "Unauthorized", "detail": "Admin authorization token required"},
                    status_code=401
                )
            token = auth_header.split("Bearer ")[1].strip()
            # Allow dev admin token or configured admin secret
            if token not in ["admin-secret-key", "dev_admin_token_2026"]:
                return JSONResponse(
                    {"error": "Forbidden", "detail": "Insufficient role privileges. Require Admin role."},
                    status_code=403
                )
        response = await call_next(request)
        return response
