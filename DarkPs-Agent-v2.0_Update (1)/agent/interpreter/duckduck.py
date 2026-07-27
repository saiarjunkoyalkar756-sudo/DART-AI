from __future__ import annotations

import re
import urllib.parse
from typing import Any

import requests


def поиск_ддг(сессия: requests.Session, запрос: str, огр: int) -> list[dict[str, str]]:
    try:
        from duckduckgo_search import DDGS
        with DDGS() as д:
            return list(д.text(запрос, max_results=огр))
    except ImportError:
        pass

    url = f'https://html.duckduckgo.com/html/?q={urllib.parse.quote(запрос)}'
    о = сессия.get(url, timeout=15)
    о.raise_for_status()
    html = о.text
    рез: list[dict[str, str]] = []
    ш = r'<a rel="nofollow" class="result__a" href="([^"]+)"[^>]*>(.*?)</a>'
    с = r'<a class="result__snippet"[^>]*>(.*?)</a>'
    сс = re.findall(ш, html)
    рс = re.findall(с, html)
    for i, (ссылка, заг) in enumerate(сс[:огр]):
        зч = re.sub(r'<[^>]+>', '', заг).strip()
        рсн = re.sub(r'<[^>]+>', '', рс[i]).strip() if i < len(рс) else ''
        рез.append({'title': зч, 'href': ссылка, 'body': рсн})
    return рез
