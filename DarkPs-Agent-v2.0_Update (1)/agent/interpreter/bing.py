from __future__ import annotations

import re
import urllib.parse

import requests


def поиск_бинг(сессия: requests.Session, запрос: str, огр: int) -> list[dict[str, str]]:
    url = f'https://www.bing.com/search?q={urllib.parse.quote(запрос)}&count={огр}'
    о = сессия.get(url, timeout=15)
    о.raise_for_status()
    html = о.text
    рез: list[dict[str, str]] = []
    бл = re.findall(r'<li class="b_algo"[^>]*>(.*?)</li>', html, re.S)
    for б in бл[:огр]:
        зм = re.search(r'<h2[^>]*>.*?<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>.*?</h2>', б, re.S)
        if зм:
            сс = зм.group(1)
            зг = re.sub(r'<[^>]+>', '', зм.group(2)).strip()
            см = re.search(r'<p[^>]*>(.*?)</p>', б, re.S)
            рс = ''
            if см:
                рс = re.sub(r'<[^>]+>', '', см.group(1)).strip()
            рез.append({'title': зг, 'href': сс, 'body': рс})
    return рез
