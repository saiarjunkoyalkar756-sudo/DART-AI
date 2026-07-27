from __future__ import annotations

import os

м = "gemini-2.5-flash"  # модель по умолчанию :|

мс = [

   # ('deepseek-v3', 'deepseek'),
    ('deepseek-v3.2', 'deepseek'),
   # ('deepseek-r1', 'deepseek'),
    ('deepseek-v4-flash', 'deepseek'),
    ('deepseek-v4-pro', 'deepseek'),

   # ('glm-4.5', 'z-ai'),
   # ('glm-4.6', 'z-ai'),
   # ('glm-4.7', 'z-ai'),
   # ('glm-5', 'z-ai'),
    ('glm-5.1', 'z-ai'),
    ('glm-5-turbo', 'z-ai'), # Fast

    ('kimi-k2.5', 'moonshotai'),
    ('kimi-k2.6', 'moonshotai'),

    ('gemini-2.5-flash', 'google'),
    ('gemini-3-flash-preview', 'google'),
   # ('gemini-3.1-flash-lite', 'google'),

   # ('gpt-5', 'darkps'),
    ('gpt-5.3-codex', 'darkps'),
   # ('gpt-5-codex', 'darkps'),
    ('gpt-5.5', 'darkps'),
   # ('gpt-5.5-chat', 'darkps'),
    ('gpt-5.5-pro', 'darkps'),
   # ('gpt-oss-120b', 'darkps'),

    # ('sonar', 'perplexity'),
    # ('sonar-deep-research', 'perplexity'),
    # ('sonar-pro', 'perplexity'),
    # ('sonar-pro-search', 'perplexity'),
    # ('sonar-reasoning-pro', 'perplexity'),

    ('qwen3-235b-a22b', 'qwen'),
    ('qwen3-coder-480b-a35b', 'qwen'),
   # ('qwen3-vl-235b-a22b-instruct', 'qwen'),

    # ('grok-4.3', 'xai'),
]


def тм() -> str:
    return os.getenv('DARKIT_MODEL', м)

# - By: T.me/sii_3