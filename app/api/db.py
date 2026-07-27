# app/api/db.py — DART AI Persistent SQLite Database Engine router
import sqlite3, os, json, uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

DB_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "dart.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                model TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                model TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (conversation_id) REFERENCES conversations (id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                google_id TEXT UNIQUE,
                email TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                picture TEXT,
                created_at TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS generations (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                prompt TEXT NOT NULL,
                result_url TEXT NOT NULL,
                metadata TEXT,
                created_at TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                icon TEXT,
                color TEXT,
                description TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS files (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                file_type TEXT NOT NULL,
                size_bytes INTEGER NOT NULL,
                content_url TEXT,
                file_data TEXT,
                project_id TEXT,
                created_at TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prompts (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                prompt_text TEXT NOT NULL,
                is_saved INTEGER DEFAULT 1,
                created_at TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS message_reactions (
                id TEXT PRIMARY KEY,
                message_id TEXT NOT NULL,
                reaction_type TEXT NOT NULL,
                comment TEXT,
                created_at TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_memories (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                memory_key TEXT NOT NULL,
                memory_value TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback_reports (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                subject TEXT NOT NULL,
                details TEXT NOT NULL,
                rating INTEGER DEFAULT 5,
                created_at TEXT NOT NULL
            )
        """)

        # ── v1.1 Production Security & Authentication Tables ─────────────────
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                uuid TEXT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT,
                google_id TEXT,
                avatar TEXT,
                role TEXT DEFAULT 'User',
                email_verified INTEGER DEFAULT 0,
                two_factor_enabled INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT,
                last_login TEXT,
                login_count INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active',
                failed_attempts INTEGER DEFAULT 0,
                locked_until TEXT
            )
        """)

        # Migration column checks for existing SQLite databases
        user_cols = [row[1] for row in cursor.execute("PRAGMA table_info(users)").fetchall()]
        cols_to_add = [
            ("uuid", "TEXT"),
            ("password_hash", "TEXT"),
            ("google_id", "TEXT"),
            ("avatar", "TEXT"),
            ("role", "TEXT DEFAULT 'User'"),
            ("email_verified", "INTEGER DEFAULT 0"),
            ("two_factor_enabled", "INTEGER DEFAULT 0"),
            ("updated_at", "TEXT"),
            ("last_login", "TEXT"),
            ("login_count", "INTEGER DEFAULT 0"),
            ("status", "TEXT DEFAULT 'active'"),
            ("failed_attempts", "INTEGER DEFAULT 0"),
            ("locked_until", "TEXT")
        ]
        for col_name, col_type in cols_to_add:
            if col_name not in user_cols:
                try:
                    cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
                except:
                    pass

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                refresh_token TEXT NOT NULL,
                ip_address TEXT,
                device TEXT,
                browser TEXT,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                last_activity TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS refresh_tokens (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                token TEXT UNIQUE NOT NULL,
                expires_at TEXT NOT NULL,
                revoked INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS password_resets (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                token TEXT UNIQUE NOT NULL,
                expires_at TEXT NOT NULL,
                used INTEGER DEFAULT 0
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS email_verifications (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                token TEXT UNIQUE NOT NULL,
                expires_at TEXT NOT NULL,
                verified INTEGER DEFAULT 0
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                action TEXT NOT NULL,
                details TEXT,
                ip_address TEXT,
                device TEXT,
                timestamp TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_keys (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                key_name TEXT NOT NULL,
                secret_hash TEXT NOT NULL,
                key_prefix TEXT NOT NULL,
                scopes TEXT NOT NULL,
                expires_at TEXT,
                last_used TEXT,
                created_at TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workspace_members (
                id TEXT PRIMARY KEY,
                workspace_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                role TEXT DEFAULT 'Viewer',
                created_at TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS two_factor (
                id TEXT PRIMARY KEY,
                user_id TEXT UNIQUE NOT NULL,
                secret_key TEXT NOT NULL,
                enabled INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS backup_codes (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                code_hash TEXT NOT NULL,
                used INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
        """)

        # ── v2.0 Autonomous Multi-Agent Swarm Tables ─────────────────────────
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS swarm_tasks (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                goal TEXT NOT NULL,
                status TEXT DEFAULT 'processing',
                result TEXT,
                created_at TEXT NOT NULL,
                completed_at TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS swarm_steps (
                id TEXT PRIMARY KEY,
                task_id TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                step_title TEXT NOT NULL,
                agent_thought TEXT,
                output TEXT,
                status TEXT DEFAULT 'completed',
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()

init_db()

class CreateConversationRequest(BaseModel):
    title: Optional[str] = "New Chat"
    model: Optional[str] = "deepseek-v3"
    parent_id: Optional[str] = None

class AddMessageRequest(BaseModel):
    role: str
    content: str
    model: Optional[str] = None

class SaveGenerationRequest(BaseModel):
    type: str
    prompt: str
    result_url: str
    metadata: Optional[dict] = {}

class CreateProjectRequest(BaseModel):
    name: str
    icon: Optional[str] = "folder"
    color: Optional[str] = "#3b82f6"
    description: Optional[str] = ""

class UploadFileRequest(BaseModel):
    name: str
    file_type: str
    size_bytes: int
    content_url: Optional[str] = None
    file_data: Optional[str] = None
    project_id: Optional[str] = None

class CreatePromptRequest(BaseModel):
    title: str
    category: str
    prompt_text: str

class MessageReactionRequest(BaseModel):
    reaction_type: str
    comment: Optional[str] = ""

@router.get("/conversations")
def list_conversations():
    with get_db() as conn:
        cursor = conn.cursor()
        rows = cursor.execute(
            "SELECT id, title, model, created_at, updated_at FROM conversations ORDER BY updated_at DESC"
        ).fetchall()
        return [dict(r) for r in rows]

@router.post("/conversations")
def create_conversation(body: CreateConversationRequest):
    cid = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO conversations (id, title, model, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (cid, body.title, body.model, now, now)
        )
        conn.commit()
    return {"id": cid, "title": body.title, "model": body.model, "created_at": now, "updated_at": now}

@router.get("/conversations/{cid}")
def get_conversation(cid: str):
    with get_db() as conn:
        cursor = conn.cursor()
        conv = cursor.execute("SELECT * FROM conversations WHERE id = ?", (cid,)).fetchone()
        if not conv:
            raise HTTPException(status_code=404, detail="Conversation not found")
        messages = cursor.execute(
            "SELECT id, role, content, model, created_at FROM messages WHERE conversation_id = ? ORDER BY created_at ASC",
            (cid,)
        ).fetchall()
        return {
            "conversation": dict(conv),
            "messages": [dict(m) for m in messages]
        }

@router.delete("/conversations/{cid}")
def delete_conversation(cid: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (cid,))
        cursor.execute("DELETE FROM conversations WHERE id = ?", (cid,))
        conn.commit()
    return {"status": "deleted", "id": cid}

@router.post("/conversations/{cid}/branch")
def branch_conversation(cid: str, from_message_id: str):
    with get_db() as conn:
        cursor = conn.cursor()
        orig = cursor.execute("SELECT * FROM conversations WHERE id = ?", (cid,)).fetchone()
        if not orig:
            raise HTTPException(status_code=404, detail="Original conversation not found")
        
        new_cid = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()
        new_title = f"{orig['title']} (Branch)"
        
        cursor.execute(
            "INSERT INTO conversations (id, title, model, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (new_cid, new_title, orig['model'], now, now)
        )
        
        msgs = cursor.execute(
            "SELECT role, content, model FROM messages WHERE conversation_id = ? AND created_at <= (SELECT created_at FROM messages WHERE id = ?) ORDER BY created_at ASC",
            (cid, from_message_id)
        ).fetchall()
        
        for m in msgs:
            cursor.execute(
                "INSERT INTO messages (id, conversation_id, role, content, model, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (str(uuid.uuid4()), new_cid, m['role'], m['content'], m['model'], now)
            )
        conn.commit()
    return {"id": new_cid, "title": new_title, "model": orig['model'], "created_at": now}

@router.get("/conversations/{cid}/export")
def export_conversation(cid: str, format: str = "markdown"):
    with get_db() as conn:
        cursor = conn.cursor()
        conv = cursor.execute("SELECT * FROM conversations WHERE id = ?", (cid,)).fetchone()
        if not conv:
            raise HTTPException(status_code=404, detail="Conversation not found")
        messages = cursor.execute(
            "SELECT role, content, model, created_at FROM messages WHERE conversation_id = ? ORDER BY created_at ASC",
            (cid,)
        ).fetchall()
        
        if format == "json":
            return {"conversation": dict(conv), "messages": [dict(m) for m in messages]}
        
        # Default Markdown
        md = f"# {conv['title']}\n\n"
        md += f"**Model:** {conv['model']} | **Date:** {conv['created_at']}\n\n---\n\n"
        for m in messages:
            role_title = "You" if m['role'] == "user" else f"DART AI ({m['model'] or 'LLM'})"
            md += f"### {role_title}\n\n{m['content']}\n\n---\n\n"
        return JSONResponse(content={"markdown": md, "title": conv['title']})

@router.post("/conversations/{cid}/messages")
def add_message(cid: str, body: AddMessageRequest):
    mid = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    with get_db() as conn:
        cursor = conn.cursor()
        conv = cursor.execute("SELECT id FROM conversations WHERE id = ?", (cid,)).fetchone()
        if not conv:
            raise HTTPException(status_code=404, detail="Conversation not found")
        cursor.execute(
            "INSERT INTO messages (id, conversation_id, role, content, model, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (mid, cid, body.role, body.content, body.model, now)
        )
        cursor.execute(
            "UPDATE conversations SET updated_at = ? WHERE id = ?",
            (now, cid)
        )
        conn.commit()
    return {"id": mid, "conversation_id": cid, "role": body.role, "content": body.content, "created_at": now}

@router.post("/messages/{mid}/reaction")
def add_reaction(mid: str, body: MessageReactionRequest):
    rid = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO message_reactions (id, message_id, reaction_type, comment, created_at) VALUES (?, ?, ?, ?, ?)",
            (rid, mid, body.reaction_type, body.comment or "", now)
        )
        conn.commit()
    return {"id": rid, "message_id": mid, "reaction": body.reaction_type}

# ── Projects API ─────────────────────────────────────────────────────────────
@router.get("/projects")
def list_projects():
    with get_db() as conn:
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM projects ORDER BY updated_at DESC").fetchall()
        return [dict(r) for r in rows]

@router.post("/projects")
def create_project(body: CreateProjectRequest):
    pid = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO projects (id, name, icon, color, description, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pid, body.name, body.icon or "folder", body.color or "#3b82f6", body.description or "", now, now)
        )
        conn.commit()
    return {"id": pid, "name": body.name, "created_at": now}

@router.delete("/projects/{pid}")
def delete_project(pid: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projects WHERE id = ?", (pid,))
        conn.commit()
    return {"status": "deleted", "id": pid}

# ── Files API ────────────────────────────────────────────────────────────────
@router.get("/files")
def list_files(project_id: Optional[str] = None):
    with get_db() as conn:
        cursor = conn.cursor()
        if project_id:
            rows = cursor.execute("SELECT * FROM files WHERE project_id = ? ORDER BY created_at DESC", (project_id,)).fetchall()
        else:
            rows = cursor.execute("SELECT * FROM files ORDER BY created_at DESC").fetchall()
        return [dict(r) for r in rows]

@router.post("/files")
def upload_file(body: UploadFileRequest):
    fid = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO files (id, name, file_type, size_bytes, content_url, file_data, project_id, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (fid, body.name, body.file_type, body.size_bytes, body.content_url or "", body.file_data or "", body.project_id or "", now)
        )
        conn.commit()
    return {"id": fid, "name": body.name, "file_type": body.file_type, "size_bytes": body.size_bytes, "created_at": now}

@router.delete("/files/{fid}")
def delete_file(fid: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM files WHERE id = ?", (fid,))
        conn.commit()
    return {"status": "deleted", "id": fid}

# ── Prompts API ──────────────────────────────────────────────────────────────
@router.get("/prompts")
def list_prompts(category: Optional[str] = None):
    with get_db() as conn:
        cursor = conn.cursor()
        if category and category != "All":
            rows = cursor.execute("SELECT * FROM prompts WHERE category = ? ORDER BY created_at DESC", (category,)).fetchall()
        else:
            rows = cursor.execute("SELECT * FROM prompts ORDER BY created_at DESC").fetchall()
        return [dict(r) for r in rows]

@router.post("/prompts")
def create_prompt(body: CreatePromptRequest):
    prid = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO prompts (id, title, category, prompt_text, is_saved, created_at) VALUES (?, ?, ?, ?, 1, ?)",
            (prid, body.title, body.category, body.prompt_text, now)
        )
        conn.commit()
    return {"id": prid, "title": body.title, "category": body.category, "created_at": now}

@router.delete("/prompts/{prid}")
def delete_prompt(prid: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM prompts WHERE id = ?", (prid,))
        conn.commit()
    return {"status": "deleted", "id": prid}

@router.post("/generations")
def save_generation(body: SaveGenerationRequest):
    gid = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    meta_json = json.dumps(body.metadata or {})
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO generations (id, type, prompt, result_url, metadata, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (gid, body.type, body.prompt, body.result_url, meta_json, now)
        )
        conn.commit()
    return {"id": gid, "type": body.type, "prompt": body.prompt, "result_url": body.result_url, "created_at": now}

@router.get("/generations")
def list_generations(gen_type: Optional[str] = None):
    with get_db() as conn:
        cursor = conn.cursor()
        if gen_type:
            rows = cursor.execute(
                "SELECT * FROM generations WHERE type = ? ORDER BY created_at DESC", (gen_type,)
            ).fetchall()
        else:
            rows = cursor.execute("SELECT * FROM generations ORDER BY created_at DESC").fetchall()
        return [dict(r) for r in rows]

