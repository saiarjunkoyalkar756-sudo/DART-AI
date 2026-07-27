from __future__ import annotations

import requests


def поиск_серп(сессия: requests.Session, запрос: str, ключ: str, огр: int) -> list[dict[str, str]]:
    url = 'https://serpapi.com/search'
    парам = {'engine': 'google', 'q': запрос, 'api_key': ключ, 'num': огр}
    о = сессия.get(url, params=парам, timeout=15)
    о.raise_for_status()
    д = о.json()
    рез: list[dict[str, str]] = []
    for э in д.get('organic_results', []):
        рез.append({'title': э.get('title', ''), 'href': э.get('link', ''), 'body': э.get('snippet', '')})
    return рез
