# app/api/queue_manager.py — Async Background Job Queue Architecture
import uuid, time
from typing import Dict, Any, Optional

JOB_QUEUE: Dict[str, Dict[str, Any]] = {}

def enqueue_job(job_type: str, payload: dict) -> str:
    """
    Enqueues a background processing job (image generation, music rendering, PDF indexing).
    """
    job_id = f"job_{uuid.uuid4().hex[:12]}"
    JOB_QUEUE[job_id] = {
        "job_id": job_id,
        "type": job_type,
        "payload": payload,
        "status": "processing",
        "created_at": time.time(),
        "result": None,
        "error": None
    }
    return job_id

def get_job_status(job_id: str) -> Optional[dict]:
    """Retrieves current job execution status and results."""
    return JOB_QUEUE.get(job_id)

def complete_job(job_id: str, result: dict):
    if job_id in JOB_QUEUE:
        JOB_QUEUE[job_id]["status"] = "completed"
        JOB_QUEUE[job_id]["result"] = result

def fail_job(job_id: str, error_msg: str):
    if job_id in JOB_QUEUE:
        JOB_QUEUE[job_id]["status"] = "failed"
        JOB_QUEUE[job_id]["error"] = error_msg
