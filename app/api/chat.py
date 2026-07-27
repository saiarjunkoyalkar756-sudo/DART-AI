# app/api/chat.py — Multi-model LLM chat router
import requests, random, string, json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
from app.api.router_engine import analyze_task_intent
from app.api.context_engine import compress_context

router = APIRouter()

MODELS = [
    {"id": "auto",               "name": "Auto (Smart Router)", "tag": "Smart",   "color": "#38bdf8"},
    {"id": "deepseek-v3",        "name": "DeepSeek V3",         "tag": "Fast",    "color": "#4ade80"},
    {"id": "deepseek-v4-flash",  "name": "DeepSeek V4 Flash",   "tag": "Flash",   "color": "#4ade80"},
    {"id": "deepseek-v4-pro",    "name": "DeepSeek V4 Pro",     "tag": "Pro",     "color": "#4ade80"},
    {"id": "deepseek-r1",        "name": "DeepSeek R1",         "tag": "Reason",  "color": "#4ade80"},
    {"id": "gpt-5",              "name": "GPT-5",               "tag": "New",     "color": "#10b981"},
    {"id": "gpt-5.5",            "name": "GPT-5.5",             "tag": "New",     "color": "#10b981"},
    {"id": "gpt-5.5-pro",        "name": "GPT-5.5 Pro",         "tag": "Pro",     "color": "#10b981"},
    {"id": "gpt-oss-120b",       "name": "GPT OSS 120B",        "tag": "Open",    "color": "#10b981"},
    {"id": "gemini-3-flash-preview", "name": "Gemini 3 Flash",  "tag": "Fast",    "color": "#818cf8"},
    {"id": "gemini-2.5-flash",   "name": "Gemini 2.5 Flash",    "tag": "Fast",    "color": "#818cf8"},
    {"id": "kimi-k2.5",          "name": "Kimi K2.5",           "tag": "Smart",   "color": "#22d3ee"},
    {"id": "kimi-k2.6",          "name": "Kimi K2.6",           "tag": "New",     "color": "#22d3ee"},
    {"id": "grok-4.3",           "name": "Grok 4.3",            "tag": "Fun",     "color": "#f472b6"},
    {"id": "qwen3-235b-a22b",    "name": "Qwen3 235B",          "tag": "Huge",    "color": "#fb923c"},
    {"id": "qwen3-coder-480b-a35b","name": "Qwen3 Coder 480B",  "tag": "Code",    "color": "#fb923c"},
    {"id": "sonar",              "name": "Sonar",               "tag": "Search",  "color": "#a78bfa"},
    {"id": "sonar-pro",          "name": "Sonar Pro",           "tag": "Pro",     "color": "#a78bfa"},
    {"id": "sonar-reasoning-pro","name": "Sonar Reasoning",     "tag": "Reason",  "color": "#a78bfa"},
    {"id": "glm-5",              "name": "GLM-5",               "tag": "New",     "color": "#f9a8d4"},
    {"id": "glm-5.1",            "name": "GLM-5.1",             "tag": "New",     "color": "#f9a8d4"},
]

def _rand(n): return ''.join(random.choices(string.ascii_letters + string.digits, k=n))
def _email(): return f"{_rand(10)}@gmail.com"
def _password(): return f"{_rand(4)}A1{_rand(4)}a!"
def _ip(): return '.'.join(str(random.randint(1, 254)) for _ in range(4))
def _ua(): return (f"Mozilla/5.0 (Linux; Android {random.randint(10,14)}; {_rand(6)}) "
                   f"AppleWebKit/537.36 (KHTML, like Gecko) "
                   f"Chrome/{random.randint(120,135)}.0.0.0 Mobile Safari/537.36")

def _get_prefix(model_id: str) -> str:
    m = model_id.lower()
    if 'glm'      in m: return 'z-ai/'
    if 'kimi'     in m: return 'moonshotai/'
    if 'gemini'   in m: return 'google/'
    if 'deepseek' in m: return 'deepseek/'
    if 'gpt'      in m: return 'openai/'
    if 'sonar'    in m: return 'perplexity/'
    if 'qwen'     in m: return 'qwen/'
    if 'grok'     in m: return 'xai/'
    return ''

_state = {"session": None, "token": None, "uid": None, "count": 0}

def _ensure_session() -> bool:
    s = _state
    if s["token"] and s["count"] < 8:
        return True

    ip = _ip()
    ua = _ua()
    sess = requests.Session()
    sess.headers.update({"User-Agent": ua, "X-Forwarded-For": ip, "X-Real-IP": ip})

    try:
        r = sess.post(
            "https://api.rewind.ai/v1/auth/signup",
            json={"email": _email(), "password": _password()},
            headers={"Content-Type": "application/json"},
            timeout=20,
        )
        data = r.json()
        s["token"] = data.get("accessToken")
        s["uid"]   = data.get("user", {}).get("id")
        s["session"] = sess
        s["count"] = 0
        return bool(s["token"])
    except:
        return False

def stream_chat(model_id: str, messages: list):
    s = _state
    if not _ensure_session():
        yield f"data: {json.dumps({'error': 'Session init failed'})}\n\n"
        return

    # Compress long conversation context
    messages = compress_context(messages)

    # Handle Smart Model Routing
    if model_id == "auto":
        last_user_msg = next((m["content"] for m in reversed(messages) if m.get("role") == "user"), "")
        analysis = analyze_task_intent(last_user_msg)
        model_id = analysis["recommended_model"]
        yield f"data: {json.dumps({'status': 'thinking', 'routed_model': analysis['model_name'], 'reason': analysis['reason']})}\n\n"

    s["session"].headers.update({
        "Authorization": f"Bearer {s['token']}",
        "x-user-id":    s["uid"],
        "Accept":       "application/json",
    })

    prefix = _get_prefix(model_id)
    full_model = prefix + model_id

    # Emit initial status steps for live thinking animation
    m_lower = model_id.lower()
    if 'sonar' in m_lower or 'search' in m_lower:
        yield f"data: {json.dumps({'status': 'searching_web'})}\n\n"
        yield f"data: {json.dumps({'status': 'reading_files'})}\n\n"
    elif 'r1' in m_lower or 'reason' in m_lower:
        yield f"data: {json.dumps({'status': 'thinking'})}\n\n"
        yield f"data: {json.dumps({'status': 'reasoning'})}\n\n"
    else:
        yield f"data: {json.dumps({'status': 'thinking'})}\n\n"

    try:
        r = s["session"].post(
            "https://api.rewind.ai/v1/chat/completions/",
            json={"messages": messages, "model": full_model, "stream": True},
            stream=True,
            timeout=(20, 180),
        )

        has_sent_writing = False
        for line in r.iter_lines(decode_unicode=True):
            if not line:
                continue
            if line.startswith("data: "):
                line = line[6:]
            if line.strip() == "[DONE]":
                break
            try:
                data = json.loads(line)
                token = data["choices"][0]["delta"].get("content")
                if token:
                    if not has_sent_writing:
                        yield f"data: {json.dumps({'status': 'writing'})}\n\n"
                        has_sent_writing = True
                    yield f"data: {json.dumps({'token': token})}\n\n"
            except:
                pass

        s["count"] += 1
        yield "data: [DONE]\n\n"

    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

class ChatRequest(BaseModel):
    model:    str = "deepseek-v3"
    messages: List[dict] = []

@router.get("/models")
def get_models():
    return MODELS

@router.post("/chat")
def chat(body: ChatRequest):
    return StreamingResponse(
        stream_chat(body.model, body.messages),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
