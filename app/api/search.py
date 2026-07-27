# app/api/search.py — AI-powered web search router
import requests, uuid, json, random, sys
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

router = APIRouter()

def _ua():
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/123.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36",
    ]
    return random.choice(agents)

def stream_search(query: str, system: str = ""):
    base = "https://www.perplexity.ai"
    ua   = _ua()
    headers = {
        "accept":           "*/*",
        "accept-language":  "en-US,en;q=0.9",
        "content-type":     "application/json",
        "origin":           base,
        "referer":          f"{base}/",
        "user-agent":       ua,
    }

    try:
        sess = requests.Session()
        sess.get(base, headers=headers, timeout=10)

        prompt_text = f"## SYSTEM:\n{system}\n\n## USER:\n{query}" if system.strip() else query

        payload = {
            "attachments":        [],
            "language":           "en-US",
            "timezone":           "Asia/Kolkata",
            "search_focus":       "internet",
            "sources":            ["web"],
            "frontend_uuid":      str(uuid.uuid4()),
            "mode":               "copilot",
            "model_preference":   "turbo",
            "is_related_query":   False,
            "is_sponsored":       False,
            "frontend_context_uuid": str(uuid.uuid4()),
            "prompt_source":      "user",
            "query_source":       "home",
            "is_incognito":       False,
            "time_from_first_type": random.uniform(3000, 20000),
            "use_schematized_api": True,
            "send_back_text_in_streaming_api": False,
            "supported_block_use_cases": [
                "answer_modes","media_items","knowledge_cards","inline_entity_cards",
                "diff_blocks","inline_images","inline_assets","refinement_filters",
            ],
            "client_coordinates": None,
            "mentions":           [],
            "dsl_query":          prompt_text,
            "skip_search_enabled": True,
            "source":             "mweb",
            "version":            "2.18",
            "rum_session_id":     str(uuid.uuid4()),
        }

        body = {"params": payload, "query_str": prompt_text}

        r = sess.post(
            "https://www.perplexity.ai/rest/sse/perplexity_ask",
            headers=headers,
            json=body,
            stream=True,
            timeout=(15, 120),
        )

        if not r.ok:
            yield f"data: {json.dumps({'error': f'Search error: {r.status_code}'})}\n\n"
            return

        for line in r.iter_lines():
            if not line:
                continue
            decoded = line.decode("utf-8")
            if not decoded.startswith("data: "):
                continue
            chunk = decoded[6:]
            if chunk == "[DONE]":
                break
            try:
                parsed = json.loads(chunk)
                for block in parsed.get("blocks", []):
                    diff = block.get("diff_block")
                    if diff and "patches" in diff:
                        for patch in diff["patches"]:
                            path = patch.get("path", "")
                            if path.startswith("/chunks"):
                                val = patch.get("value")
                                if isinstance(val, str):
                                    yield f"data: {json.dumps({'token': val})}\n\n"
                                elif isinstance(val, list):
                                    for v in val:
                                        if isinstance(v, str):
                                            yield f"data: {json.dumps({'token': v})}\n\n"
            except json.JSONDecodeError:
                pass

        yield "data: [DONE]\n\n"

    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

class SearchRequest(BaseModel):
    query:  str
    system: str = ""

@router.post("/search")
def search(body: SearchRequest):
    return StreamingResponse(
        stream_search(body.query, body.system),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
