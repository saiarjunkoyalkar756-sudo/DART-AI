from __future__ import annotations

import requests


def поиск_брейв(сессия: requests.Session, запрос: str, ключ: str, огр: int) -> list[dict[str, str]]:
    url = 'https://api.search.brave.com/res/v1/web/search'
    заг = {'X-Subscription-Token': ключ, 'Accept': 'application/json'}
    парам = {
        'q': запрос, 'count': огр, 'offset': 0, 'mkt': 'en-US', 'safesearch': 'moderate',
        'freshness': 'all', 'text_decorations': False, 'text_snippet': True,
    }
    о = сессия.get(url, headers=заг, params=парам, timeout=15)
    о.raise_for_status()
    д = о.json()
    рез: list[dict[str, str]] = []
    for э in д.get('web', {}).get('results', []):
        рез.append({'title': э.get('title', ''), 'href': э.get('url', ''), 'body': э.get('description', '')})
    return рез
