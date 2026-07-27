# app/middleware/rate_limit.py — In-Memory Rate Limiting Middleware
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 120, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.clients = {}  # ip -> (count, reset_time)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "127.0.0.1"
        now = time.time()

        # Clean old windows
        if client_ip in self.clients:
            count, reset_time = self.clients[client_ip]
            if now > reset_time:
                self.clients[client_ip] = (1, now + self.window_seconds)
            else:
                if count >= self.max_requests:
                    return JSONResponse(
                        {"error": "Too Many Requests", "detail": f"Rate limit exceeded ({self.max_requests} req/{self.window_seconds}s)"},
                        status_code=429
                    )
                self.clients[client_ip] = (count + 1, reset_time)
        else:
            self.clients[client_ip] = (1, now + self.window_seconds)

        response = await call_next(request)
        return response
