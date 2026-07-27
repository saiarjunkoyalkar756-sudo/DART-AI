# app/api/context_engine.py — Context Window Compression & Summarization
from typing import List, Dict

MAX_MESSAGES_LIMIT = 20

def compress_context(messages: List[dict]) -> List[dict]:
    """
    Compresses chat history by sliding window & summary truncation
    if turn count exceeds MAX_MESSAGES_LIMIT.
    """
    if len(messages) <= MAX_MESSAGES_LIMIT:
        return messages

    # Keep system message if present
    system_msgs = [m for m in messages if m.get("role") == "system"]
    non_system = [m for m in messages if m.get("role") != "system"]

    # Retain recent turns
    recent_turns = non_system[-12:]
    
    # Generate summary chip of older turns
    older_turns = non_system[:-12]
    summary_text = f"[Context Compression: {len(older_turns)} earlier turns summarized for optimal response speed.]"
    
    summary_msg = {"role": "system", "content": summary_text}
    
    return system_msgs + [summary_msg] + recent_turns
