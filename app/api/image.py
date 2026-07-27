# app/api/image.py — AI Image Generation router via Pollinations.ai
import requests, json, random, urllib.parse
from fastapi import APIRouter
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

MODELS = [
    {"id": "flux",            "name": "FLUX",              "tag": "Best",    "desc": "Highest quality photorealistic"},
    {"id": "flux-realism",    "name": "FLUX Realism",      "tag": "Photo",   "desc": "Hyper-realistic photography"},
    {"id": "flux-anime",      "name": "FLUX Anime",        "tag": "Anime",   "desc": "Japanese animation style"},
    {"id": "flux-3d",         "name": "FLUX 3D",           "tag": "3D",      "desc": "3D rendered scenes"},
    {"id": "turbo",           "name": "Turbo",             "tag": "Fast",    "desc": "Fastest generation"},
    {"id": "gptimage",        "name": "GPT Image",         "tag": "GPT",     "desc": "OpenAI image quality"},
]

STYLE_PRESETS = [
    {"id": "",             "name": "None",         "suffix": ""},
    {"id": "cinematic",    "name": "Cinematic",    "suffix": ", cinematic lighting, dramatic, 4K, film grain"},
    {"id": "anime",        "name": "Anime",        "suffix": ", anime style, vibrant colors, detailed, studio quality"},
    {"id": "photorealism", "name": "Photo",        "suffix": ", photorealistic, DSLR, 8K resolution, sharp focus"},
    {"id": "digital-art",  "name": "Digital Art",  "suffix": ", digital art, concept art, highly detailed, ArtStation"},
    {"id": "oil-painting", "name": "Oil Paint",    "suffix": ", oil painting, classical art style, museum quality"},
    {"id": "watercolor",   "name": "Watercolor",   "suffix": ", watercolor painting, soft colors, artistic"},
    {"id": "pixel-art",    "name": "Pixel Art",    "suffix": ", pixel art, retro gaming style, 16-bit"},
]

SIZES = {
    "square":    (1024, 1024),
    "landscape": (1280, 720),
    "portrait":  (720, 1280),
    "wide":      (1920, 1080),
}

class ImageRequest(BaseModel):
    prompt:  str
    model:   str = "flux"
    style:   str = ""
    size:    str = "square"
    seed:    Optional[int] = None

@router.get("/image/models")
def get_image_models():
    return MODELS

@router.get("/image/styles")
def get_image_styles():
    return STYLE_PRESETS

@router.post("/image/generate")
def generate_image(body: ImageRequest):
    suffix = ""
    for s in STYLE_PRESETS:
        if s["id"] == body.style:
            suffix = s["suffix"]
            break

    full_prompt = body.prompt.strip() + suffix
    encoded     = urllib.parse.quote(full_prompt)
    w, h = SIZES.get(body.size, (1024, 1024))
    seed = body.seed if body.seed is not None else random.randint(1, 999999)
    model = body.model if body.model in [m["id"] for m in MODELS] else "flux"

    img_url = (
        f"https://image.pollinations.ai/prompt/{encoded}"
        f"?width={w}&height={h}&model={model}&seed={seed}&nologo=true&enhance=true"
    )

    return {
        "url":    img_url,
        "prompt": full_prompt,
        "seed":   seed,
        "width":  w,
        "height": h,
        "model":  model,
    }

@router.get("/image/proxy")
def proxy_image(url: str):
    try:
        r = requests.get(url, timeout=60, stream=True)
        if r.status_code != 200:
            return JSONResponse({"error": "Image not found"}, status_code=404)
        return StreamingResponse(
            r.iter_content(chunk_size=8192),
            media_type=r.headers.get("content-type", "image/jpeg"),
            headers={"Cache-Control": "public, max-age=86400"},
        )
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
