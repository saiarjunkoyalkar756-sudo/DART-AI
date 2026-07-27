from __future__ import annotations

import os

import requests


def поиск_гугл(сессия: requests.Session, запрос: str, ключ: str, огр: int) -> list[dict[str, str]]:

    сх = os.getenv('GOOGLE_SEARCH_CX', '') # Поместите свои жетон сюда :)
    
    
    if not сх:
        return []
    url = 'https://www.googleapis.com/customsearch/v1'
    парам = {'key': ключ, 'cx': сх, 'q': запрос, 'num': огр}
    о = сессия.get(url, params=парам, timeout=15)
    о.raise_for_status()
    д = о.json()
    рез: list[dict[str, str]] = []
    for э in д.get('items', []):
        рез.append({'title': э.get('title', ''), 'href': э.get('link', ''), 'body': э.get('snippet', '')})
    return рез
