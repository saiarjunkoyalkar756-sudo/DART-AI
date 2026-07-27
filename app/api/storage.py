# app/api/storage.py — S3-Compatible Object Storage Abstraction Engine
import os, uuid
from typing import Optional

STORAGE_DIR = "app/data/uploads"
os.makedirs(STORAGE_DIR, exist_ok=True)

def save_blob(filename: str, data: bytes, content_type: str = "application/octet-stream") -> dict:
    """
    Saves binary blob content to Object Storage and returns media metadata.
    """
    file_ext = os.path.splitext(filename)[1]
    unique_name = f"{uuid.uuid4().hex[:12]}{file_ext}"
    target_path = os.path.join(STORAGE_DIR, unique_name)

    with open(target_path, "wb") as f:
        f.write(data)

    return {
        "file_id": unique_name,
        "original_name": filename,
        "path": target_path,
        "url": f"/static/uploads/{unique_name}",
        "size_bytes": len(data),
        "content_type": content_type
    }

def get_blob_path(file_id: str) -> Optional[str]:
    path = os.path.join(STORAGE_DIR, file_id)
    if os.path.exists(path):
        return path
    return None

def delete_blob(file_id: str) -> bool:
    path = os.path.join(STORAGE_DIR, file_id)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False
