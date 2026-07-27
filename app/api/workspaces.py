# app/api/workspaces.py — Workspaces & Workspace Members Manager Router
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.api.db import get_db

router = APIRouter()

class CreateWorkspaceRequest(BaseModel):
    name: str

class AddMemberRequest(BaseModel):
    email: str
    role: str = "Editor"  # Owner | Admin | Editor | Viewer

@router.get("/workspaces")
def get_user_workspaces(request: Request):
    user = getattr(request.state, "user", None)
    uid = user["id"] if user else "dev_user"
    return [
        {"id": "personal", "name": "Personal Workspace", "role": "Owner", "is_default": True},
        {"id": "work",     "name": "Work Workspace",     "role": "Admin", "is_default": False},
        {"id": "school",   "name": "School Workspace",   "role": "Editor", "is_default": False},
        {"id": "client",   "name": "Client Project",     "role": "Viewer", "is_default": False}
    ]

@router.post("/workspaces")
def create_workspace(body: CreateWorkspaceRequest, request: Request):
    wid = str(uuid.uuid4())
    user = getattr(request.state, "user", None)
    uid = user["id"] if user else "dev_user"
    now = datetime.now(timezone.utc).isoformat()
    return {"id": wid, "name": body.name, "role": "Owner", "created_at": now}

@router.get("/workspaces/{workspace_id}/members")
def get_workspace_members(workspace_id: str):
    now = datetime.now(timezone.utc).isoformat()
    return [
        {"id": "mem_1", "user_id": "dev_user", "name": "Dev User", "email": "dev.user@gmail.com", "role": "Owner", "joined_at": now},
        {"id": "mem_2", "user_id": "user_2", "name": "Alex Smith", "email": "alex@studio.com", "role": "Editor", "joined_at": now}
    ]

@router.post("/workspaces/{workspace_id}/members")
def add_workspace_member(workspace_id: str, body: AddMemberRequest):
    mid = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    return {"id": mid, "workspace_id": workspace_id, "email": body.email, "role": body.role, "joined_at": now}
