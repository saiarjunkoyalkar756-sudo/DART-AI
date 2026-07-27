# app/api/memories.py — User AI Memories API Router
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.api.db import get_db

router = APIRouter()

class MemoryCreate(BaseModel):
    user_id: str = "dev_user"
    memory_key: str
    memory_value: str

@router.get("/memories")
def get_user_memories(user_id: str = "dev_user"):
    with get_db() as conn:
        cursor = conn.cursor()
        rows = cursor.execute(
            "SELECT id, user_id, memory_key, memory_value, created_at FROM user_memories WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        ).fetchall()
        return [
            {"id": r[0], "user_id": r[1], "key": r[2], "value": r[3], "created_at": r[4]}
            for r in rows
        ]

@router.post("/memories")
def add_user_memory(body: MemoryCreate):
    mid = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user_memories (id, user_id, memory_key, memory_value, created_at) VALUES (?, ?, ?, ?, ?)",
            (mid, body.user_id, body.memory_key, body.memory_value, now)
        )
        conn.commit()
    return {"id": mid, "key": body.memory_key, "value": body.memory_value, "created_at": now}

@router.delete("/memories/{memory_id}")
def delete_user_memory(memory_id: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_memories WHERE id = ?", (memory_id,))
        conn.commit()
    return {"status": "deleted", "id": memory_id}
