# app/api/router_engine.py — Smart Task Intent Classifier & Model Router
import re

def analyze_task_intent(prompt: str) -> dict:
    text = prompt.lower()

    # Code Intent Detection
    code_keywords = ['code', 'python', 'javascript', 'html', 'css', 'react', 'sql', 'function', 'def ', 'class ', 'import ', 'bug', 'fix', 'refactor', 'api', 'json', 'typescript', 'algorithm']
    if any(k in text for k in code_keywords):
        return {
            "intent": "code",
            "recommended_model": "qwen3-coder-480b-a35b",
            "model_name": "Qwen3 Coder 480B",
            "reason": "Detected coding / software engineering task"
        }

    # Reasoning / Math Intent Detection
    reasoning_keywords = ['solve', 'proof', 'math', 'quantum', 'derive', 'equation', 'physics', 'calculate', 'explain why', 'step by step', 'logic']
    if any(k in text for k in reasoning_keywords):
        return {
            "intent": "reasoning",
            "recommended_model": "deepseek-r1",
            "model_name": "DeepSeek R1",
            "reason": "Detected complex reasoning / math problem"
        }

    # Web Search Intent Detection
    search_keywords = ['search', 'latest', 'news', 'today', 'price', 'weather', 'who is', 'current', '2026', 'release', 'recent']
    if any(k in text for k in search_keywords):
        return {
            "intent": "search",
            "recommended_model": "sonar-pro",
            "model_name": "Sonar Pro (Search)",
            "reason": "Detected live web search query"
        }

    # Default / General Intent -> High Performance GPT-5.5 / DeepSeek V3
    return {
        "intent": "general",
        "recommended_model": "gpt-5.5",
        "model_name": "GPT-5.5",
        "reason": "General conversational / creative task"
    }
