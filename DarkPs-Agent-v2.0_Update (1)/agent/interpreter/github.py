from __future__ import annotations

import base64
import os
import urllib.parse
from pathlib import Path
from typing import Any

import requests

#     было циклического импорта >_

_с0 = '\033[0m'
_с1 = '\033[1m'
_сж = '\033[33m'
_сс = '\033[34m'
_сб = '\033[37m'
_с92 = '\033[92m'
_ср = '\033[31m'
_сз = '\033[32m'


def _цв(т: str, ц: str = _сб, ж: bool = False) -> str:
    import sys
    if os.getenv('NO_COLOR') or not sys.stdout.isatty():
        return т
    return (_с1 if ж else '') + ц + т + _с0


def гт() -> str:
    ткн = os.getenv('GITHUB_TOKEN')
    if ткн:
        return ткн
    пт_срд = Path.home() / '.darkps' / '.env'
    if пт_срд.exists():
        for line in пт_срд.read_text().splitlines():
            if line.startswith('GITHUB_TOKEN='):
                return line.split('=', 1)[1].strip().strip('"').strip("'")
    return ''


def сгт(ткн: str) -> None:
    д = Path.home() / '.darkps'
    д.mkdir(parents=True, exist_ok=True)
    п = д / '.env'
    стрк = []
    if п.exists():
        стрк = п.read_text().splitlines()
    нстрк = []
    найд = False
    for line in стрк:
        if line.startswith('GITHUB_TOKEN='):
            нстрк.append(f'GITHUB_TOKEN={ткн}')
            найд = True
        else:
            нстрк.append(line)
    if not найд:
        нстрк.append(f'GITHUB_TOKEN={ткн}')
    п.write_text('\n'.join(нстрк) + '\n')


def пгт(ткн: str) -> bool:
    try:
        отв = requests.get(
            'https://api.github.com/user',
            headers={'Authorization': f'token {ткн}', 'Accept': 'application/vnd.github.v3+json'},
            timeout=10,
        )
        return отв.status_code == 200
    except Exception:
        return False


def угт() -> str:
    ткн = гт()
    while not ткн or not пгт(ткн):
        if not ткн:
            print(_цв('\n— GitHub token is required\n', _сж, ж=True))
        else:
            print(_цв('\n- Invalid token', _ср, ж=True))
        print(_цв('1. Open -- ' + _сс + 'https://github.com/settings/tokens' + _сб, _сб))
        print(_цв('2. Click "' + _сж + 'Generate new token (classic)' + _сб + '"', _сб))
        print(_цв('3. Choose: ' + _с92 + 'repo' + _сб + ', ' + _с92 + 'read:user' + _сб + ', ' + _с92 + 'read:org' + _сб, _сб))
        print(_цв('4. Paste the token:', _сб))
        ткн = input(_цв('\nToken: ', _сж)).strip()
        if not ткн:
            print(_цв('- Token is required', _ср))
            continue
        сгт(ткн)
        os.environ['GITHUB_TOKEN'] = ткн
        if пгт(ткн):
            print(_цв('-- Token saved\n', _сз, ж=True))
            break
        else:
            print(_цв('-- Invalid token\n', _ср, ж=True))
    return ткн


def гп(зап: str) -> str:
    ткн = угт()
    try:
        url = f'https://api.github.com/search/repositories?q={urllib.parse.quote(зап)}&per_page=10'
        отв = requests.get(url, headers={'Authorization': f'token {ткн}', 'Accept': 'application/vnd.github.v3+json'}, timeout=15)
        отв.raise_for_status()
        д = отв.json()
        эл = д.get('items', [])
        if not эл:
            return f'- Нет репозиториев: "{зап}"'
        рз = []
        for i, item in enumerate(эл, 1):
            рз.append(f"{i}. {item['full_name']}\n   ⭐ {item.get('stargazers_count', 0)} | {item.get('description', 'No description')}\n   {item['html_url']}")
        return '\n'.join(рз)
    except Exception as e:
        return f'- GitHub Error: {e}'


def гр(рп: str) -> str:
    ткн = угт()
    try:
        url = f'https://api.github.com/repos/{рп}'
        отв = requests.get(url, headers={'Authorization': f'token {ткн}', 'Accept': 'application/vnd.github.v3+json'}, timeout=15)
        отв.raise_for_status()
        д = отв.json()
        стрк = [
            f"Repo: {д['full_name']}",
            f"Description: {д.get('description', 'Н/Д')}",
            f"⭐ {д.get('stargazers_count', 0)} | 🍴 {д.get('forks_count', 0)} | ⚠ {д.get('open_issues_count', 0)}",
            f"Language: {д.get('language', 'Н/Д')}",
            f"Branch: {д.get('default_branch', 'main')}",
            f"URL: {д['html_url']}",
        ]
        return '\n'.join(стрк)
    except Exception as e:
        return f'- Repo error: {e}'


def гс(рп: str, пт: str, втк: str = 'main') -> str:
    ткн = угт()
    try:
        url = f'https://api.github.com/repos/{рп}/contents/{пт}?ref={втк}'
        отв = requests.get(url, headers={'Authorization': f'token {ткн}', 'Accept': 'application/vnd.github.v3+json'}, timeout=15)
        отв.raise_for_status()
        д = отв.json()
        if isinstance(д, list):
            эл = [f"{'[ПАП]' if item['type'] == 'dir' else '[ФАЙЛ]'} {item['name']}" for item in д]
            return f'- Contents {рп}/{пт}:\n' + '\n'.join(эл)
        else:
            сдр = base64.b64decode(д.get('content', '')).decode('utf-8', errors='replace')
            return сдр
    except Exception as e:
        return f'- Read error: {e}'
