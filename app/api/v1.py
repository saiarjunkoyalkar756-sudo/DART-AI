# app/api/v1.py — Public Developer API v1 Router
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.api.chat import MODELS, stream_chat

router = APIRouter()

API_KEYS = {
    "dart_sk_live_demo12345": {"name": "Demo Application Key", "rate_limit": 1000}
}

class ChatCompletionRequest(BaseModel):
    model: str = "deepseek-v3"
    messages: List[dict]
    stream: Optional[bool] = False

@router.get("/v1/models")
def list_v1_models(x_api_key: Optional[str] = Header(None)):
    return {"object": "list", "data": MODELS}

@router.post("/v1/chat/completions")
def create_chat_completion(body: ChatCompletionRequest, x_api_key: Optional[str] = Header(None)):
    if body.stream:
        return StreamingResponse(
            stream_chat(body.model, body.messages),
            media_type="text/event-stream"
        )
    return {
        "id": f"chatcmpl-{uuid.uuid4().hex[:12]}",
        "object": "chat.completion",
        "created": int(datetime.now(timezone.utc).timestamp()),
        "model": body.model,
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": "DART AI API v1 endpoint response."},
            "finish_reason": "stop"
        }]
    }

@router.post("/v1/api-keys")
def generate_api_key(key_name: str = "Developer Key"):
    new_key = f"dart_sk_live_{uuid.uuid4().hex[:16]}"
    API_KEYS[new_key] = {"name": key_name, "rate_limit": 1000}
    return {"api_key": new_key, "name": key_name, "status": "active"}
