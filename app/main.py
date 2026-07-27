# app/main.py — Production FastAPI Application Entrypoint
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from app.config import settings
from app.middleware.security import SecurityHeadersMiddleware

from app.api.chat   import router as chat_router
from app.api.search import router as search_router
from app.api.tts    import router as tts_router
from app.api.music  import router as music_router
from app.api.mail   import router as mail_router
from app.api.image  import router as image_router
from app.api.db     import router as db_router
from app.api.auth   import router as auth_router
from app.api.users  import router as users_router
from app.api.security import router as security_router
from app.api.sessions import router as sessions_router
from app.api.api_keys import router as api_keys_router
from app.api.workspaces import router as workspaces_router
from app.api.analytics import router as analytics_router
from app.api.memories  import router as memories_router
from app.api.admin      import router as admin_router
from app.api.swarm      import router as swarm_router
from app.api.v1         import router as v1_router

from app.middleware.security_headers import SecurityHeadersMiddleware
from app.middleware.csrf import CSRFMiddleware
from app.middleware.auth import AuthMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.auth_rbac  import RBACMiddleware

app = FastAPI(
    title=settings.title,
    version=settings.version,
    docs_url="/docs",
    redoc_url=None
)

# Hardened CORS Settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Security Middleware Pipeline
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware, max_requests=120, window_seconds=60)
app.add_middleware(CSRFMiddleware)
app.add_middleware(AuthMiddleware)
app.add_middleware(RBACMiddleware)

# Production Liveness Health Check
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": settings.title, "version": settings.version}

app.include_router(chat_router,       prefix="/api")
app.include_router(search_router,     prefix="/api")
app.include_router(tts_router,        prefix="/api")
app.include_router(music_router,      prefix="/api")
app.include_router(mail_router,       prefix="/api")
app.include_router(image_router,      prefix="/api")
app.include_router(db_router,         prefix="/api")
app.include_router(auth_router,       prefix="/api")
app.include_router(users_router,      prefix="/api")
app.include_router(security_router,   prefix="/api")
app.include_router(sessions_router,   prefix="/api")
app.include_router(api_keys_router,   prefix="/api")
app.include_router(workspaces_router, prefix="/api")
app.include_router(analytics_router,  prefix="/api")
app.include_router(memories_router,   prefix="/api")
app.include_router(admin_router,      prefix="/api")
app.include_router(swarm_router,      prefix="/api")
app.include_router(v1_router)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/{full_path:path}")
def catch_all(full_path: str):
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return JSONResponse({"error": "Static file not found"}, status_code=404)
