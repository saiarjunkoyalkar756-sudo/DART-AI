# - @2026 | Version 2.0
# - Created By: T.me/sii_3
# - Mr Dark

# ~ Agent DarkPs Official [>_]

from __future__ import annotations

dark = "t.me/sii_3"
версия = "Выпустобщено в @2026"

import json
import os
import sys
import random
import string
import time

from typing import Iterable
from model import м

import requests

_рк = {
    "reasoning_content",
    "reasoning",
    "think",
    "thinking",
    "analysis",
    "thoughts",
    "мышление",
    "reason",
}


def сарай(жа=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=жа))


def пз():
    return f"{сарай(6)}@gmail.com"


def че():
    return f"{сарай(4)}A1{сарай(4)}a"


def рк():
    return f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"


def жк():
    return f"Mozilla/5.0 (Linux; Android {random.randint(10,14)}; {сарай(6)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(120,135)}.0.0.0 Mobile Safari/537.36"


def _провайдер(имя: str) -> str:
    low = имя.lower()
    if "glm" in low:
        return "z-ai"
    if "kimi" in low:
        return "moonshotai"
    if "gemini" in low:
        return "google"
    if "deepseek" in low:
        return "deepseek"
    if low.startswith("gpt") or "gpt" in low:
        return "openai"
    if "qwen" in low:
        return "qwen"
    if "grok" in low:
        return "xai"
    if "sonar" in low:
        return "perplexity"
    return "darkps"


def _н(список):
    return ''.join(chr(элемент) for элемент in список)


def проверка():
    к_имя = _н([100, 97, 114, 107])
    к_знач = _н([116, 46, 109, 101, 47, 115, 105, 105, 95, 51])
    в_имя = _н([1074, 1077, 1088, 1089, 1080, 1103])
    в_знач = _н([1042, 1099, 1087, 1091, 1089, 1090, 1086, 1073, 1097, 1077, 1085, 1086, 32, 1074, 32, 64, 50, 48, 50, 54])
    ошибка = globals().get(к_имя) != к_знач or globals().get(в_имя) != в_знач
    if ошибка:
        sys.stdout.write(_н([1058, 1099, 32, 1095, 1090, 1086, 44, 32, 1074, 1084, 1077, 1096, 1080, 1074, 1089, 1103, 32, 1074, 32, 1082, 1086, 1076, 44, 32, 1080, 1076, 1080, 1086, 1090, 63, 32, 58, 124]) + '\n')
        sys.stdout.flush()
        raise SystemExit


проверка()


def создать_сессию():
    дй = пз()
    жопае = че()
    уретра = рк()
    хи = жк()
    кк = requests.Session()
    кк.headers.update({
        'User-Agent': хи,
        'X-Forwarded-For': уретра,
        'X-Real-IP': уретра,
        'X-Originating-IP': уретра
    })
    за = кк.post('https://api.rewind.ai/v1/auth/signup',
                 json={'email': дй, 'password': жопае},
                 headers={'Content-Type': 'application/json'})
    вуайеристж = за.json()
    уй = вуайеристж.get('accessToken')
    if not уй:
        raise Exception(f"- AccessToken: {вуайеристж}")
    чб = вуайеристж['user']['id']
    кк.headers.update({
        'Authorization': f"Bearer {уй}",
        'x-user-id': чб,
        'Accept': 'application/json'
    })
    return кк, уй, чб


def _л(р: requests.Response) -> Iterable[str]:
    for line in р.iter_lines(decode_unicode=True):
        if line is None:
            continue
        line = line.strip()
        if line:
            yield line


def з(м, с):

    м_имя = (м or "").strip()
    if not м_имя:
        м_имя = м

    if "/" in м_имя:
        model_full = м_имя
    else:
        prov = _провайдер(м_имя)
        model_full = f"{prov}/{м_имя}"

    смс = list(с or [])

    for msg in смс:
        if msg.get('content') is None:
            msg['content'] = ''
        if not isinstance(msg.get('content'), str):
            msg['content'] = str(msg.get('content')) if msg.get('content') is not None else ''

    for msg in смс:
        if msg.get('content') is None:
            msg['content'] = ''
        if not isinstance(msg.get('content'), str):
            msg['content'] = str(msg['content']) if msg.get('content') is not None else ''

    попытка = 0
    макс_попыток = 3

    while попытка < макс_попыток:
        сессия = None
        try:
            сессия, токен, ид = создать_сессию()

            запрос = сессия.post(
                'https://api.rewind.ai/v1/chat/completions/',
                json={
                    'messages': смс,
                    'model': model_full,
                    'stream': True
                },
                stream=True,
                timeout=(15, 300)
            )

            if 400 <= запрос.status_code < 500:
                if запрос.status_code == 429:
                    попытка += 1
                    time.sleep(2)
                    if сессия:
                        сессия.close()
                    continue
                err_text = ""
                try:
                    err_text = запрос.text[:500]
                except Exception:
                    pass
                yield {"тип": "ответ", "текст": f"\n- {запрос.status_code}: {err_text}\n"}
                if сессия:
                    сессия.close()
                return

            запрос.raise_for_status()
            э = False

            for стр in _л(запрос):
                лн = стр

                if лн.startswith("data:"):
                    лн = лн[5:].strip()

                if лн == "[DONE]":
                    break

                try:
                    до = json.loads(лн)
                    delta = до.get('choices', [{}])[0].get('delta', {})

                    повязка = delta.get('content')
                    if повязка:
                        yield {"тип": "ответ", "текст": повязка}
                        э = True

                    for rk in _рк:
                        think = delta.get(rk)
                        if think:
                            yield {"тип": "мышление", "текст": str(think)}
                            э = True
                            break

                    tool_calls = delta.get('tool_calls')
                    if tool_calls:
                        yield {"тип": "tool", "текст": json.dumps(tool_calls)}
                        э = True

                except Exception:
                    if лн:
                        yield {"тип": "ответ", "текст": лн}
                        э = True

            if not э and запрос.text:
                т = запрос.text.strip()
                if т:
                    try:
                        jd = json.loads(т)
                        msg = jd.get('choices', [{}])[0].get('message', {})
                        content = msg.get('content') or msg.get('text', '')
                        if content:
                            yield {"тип": "ответ", "текст": content}
                        for rk in _рк:
                            think = msg.get(rk)
                            if think:
                                yield {"тип": "мышление", "текст": str(think)}
                                break
                    except Exception:
                        yield {"тип": "ответ", "текст": т}

            запрос.close()
            if сессия:
                сессия.close()
            break

        except requests.exceptions.HTTPError as e:
            if сессия:
                сессия.close()
            yield {"тип": "ответ", "текст": f"\n- {str(e)[:200]}\n"}
            break

        except Exception as e:
            if сессия:
                сессия.close()
            yield {"тип": "ответ", "текст": f"\n- {str(e)[:200]}\n"}
            break


if __name__ == "__main__":
    raw = sys.stdin.read().strip()
    if raw:
        вход = json.loads(raw)
    else:
        вход = {"model": "", "messages": []}

    for part in з(
        вход.get("model", ""),
        вход.get("messages", []),
    ):
        print(json.dumps(part, ensure_ascii=False), flush=True)
        
# - By: T.me/sii_3