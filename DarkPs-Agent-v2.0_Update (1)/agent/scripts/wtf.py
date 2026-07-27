# - @2026 | Version 2.0
# - Created By: T.me/sii_3
# - Mr Dark

# ~ Agent DarkPs Official [>_]

from __future__ import annotations

dark="t.me/sii_3"
версия="Выпустобщено в @2026"

import os
import random
import string
import sys
import time

from typing import Any
from api import з as з_у
import requests
from model import мс as _мс, тм as _текущая_модель

_онлайн_модели:list[tuple[str,str]]=[]

def _н(мс:list[Any]|None=None)->list[dict[str,str]]:
    срк=list(_мс if мс is None else мс)
    вых=[]
    for э in срк:
        if isinstance(э,dict):
            и=str(э.get('name') or э.get('имя') or '').strip()
            пв=str(э.get('provider') or э.get('провайдер') or '').strip()
        elif isinstance(э,(list,tuple)) and len(э)>=2:
            и=str(э[0]).strip()
            пв=str(э[1]).strip()
        elif isinstance(э,str):
            и=э.strip()
            пв=''
        else:
            continue
        if not и:
            continue
        пв=пв or 'darkps'
        вых.append({
            'name':и,
            'provider':пв,
            'id':f'{пв}/{и}',
            'label':и
        })
    return вых

def _ук(мс:list[Any])->None:
    global _онлайн_модели
    _онлайн_модели=[(x['name'],x['provider']) for x in _н(мс)]

def _сл()->list[tuple[str,str]]:
    return list(_мс)

def тм()->str:
    return os.getenv('DARKIT_MODEL',_текущая_модель())

def мс()->list[tuple[str,str]]:
    return list(_онлайн_модели)

def сл(н:int=8)->str:
    алф=string.ascii_lowercase+string.digits
    return ''.join(random.choice(алф) for _ in range(н))

def пч()->str:
    return f'{сл(10)}@gmail.com'

def пароль()->str:
    return f'{сл(4)}A1{сл(4)}a'

def зг()->dict[str,str]:
    ua=f'Mozilla/5.0 (Linux; Android {random.randint(10,14)}; {сл(6)}) AppleWebKit/537.36'
    return {
        'User-Agent':ua,
        'X-Forwarded-For':'.'.join(str(random.randint(1,254)) for _ in range(4)),
        'X-Real-IP':'.'.join(str(random.randint(1,254)) for _ in range(4))
    }

def _провайдер(и:str)->str:
    low=и.lower()
    if 'glm' in low:return 'z-ai'
    if 'kimi' in low:return 'moonshotai'
    if 'gemini' in low:return 'google'
    if 'deepseek' in low:return 'deepseek'
    if 'gpt' in low:return 'darkps'
    if 'sonar' in low:return 'perplexity'
    if 'qwen' in low:return 'qwen'
    if 'grok' in low:return 'xai'
    if 'darkit' in low:return 'darkit'
    return 'darkps'

def _id_модели(и:str)->str:
    и=и.strip()
    if not и:return 'darkps/darkps'
    if '/' in и:return и
    return f'{_провайдер(и)}/{и}'

def рг(сс:requests.Session)->tuple[str,str]:
    return os.getenv('DARK_TOKEN',''),os.getenv('DARK_USER_ID','')

def _д(список):
    return ''.join(chr(элемент) for элемент in список)

def проверка():
    к_имя=_д([100,97,114,107])
    к_знач=_д([116,46,109,101,47,115,105,105,95,51])
    в_имя=_д([1074,1077,1088,1089,1080,1103])
    в_знач=_д([1042,1099,1087,1091,1089,1090,1086,1073,1097,1077,1085,1086,32,1074,32,64,50,48,50,54])
    if globals().get(к_имя)!=к_знач or globals().get(в_имя)!=в_знач:
        sys.stdout.write(_д([1058,1099,32,1095,1090,1086,44,32,1074,1084,1077,1096,1080,1074,1072,1083,1089,1103,32,1074,32,1082,1086,1076,44,32,1080,1076,1080,1086,1090,63,32,58,124])+'\n')
        sys.stdout.flush()
        raise SystemExit

проверка()

def по(сс:requests.Session,ткн:str,мдл:str,смс:list[dict[str,str]]):
    for кусок in з_у(мдл,смс):
        if isinstance(кусок,dict):
            тип=str(кусок.get("тип") or кусок.get("type") or "").strip().lower()
            текст=кусок.get("текст") or кусок.get("text")
            if not текст:
                continue
            текст=str(текст)
            if тип in {"мышление","thinking","reasoning","thought"}:
                yield f"THINK: {текст}"
            elif тип in {"tool","tools","action"}:
                yield f"TOOL: {текст}"
            else:
                yield текст
        elif кусок is not None:
            yield str(кусок)


def вм() -> str:
    from ps.dark import цв, сж, с35, сб, ср, с90

    режим = os.getenv('DARKIT_MODE', 'local').lower()

    if режим == 'local':
        return тм()

    if not _онлайн_модели:
        _ук(_сл())

    if not _онлайн_модели:
        return тм()

    print(цв('\n- All Models DarkPs Agent :)\n', сж))

    for i, (и, _) in enumerate(_онлайн_модели, 1):
        print(цв(f'{i:02d}. {и}', с35), flush=True)
        time.sleep(0.03)

    в = input(цв(f'\n\nModel - [{тм()}] - skip > ', сж)).strip()

    if not в:
        return тм()

    if в.isdigit():
        ид = int(в) - 1
        if 0 <= ид < len(_онлайн_модели):
            return _онлайн_модели[ид][0]

    for и, _ in _онлайн_модели:
        if в.lower() == и.lower():
            return и

    print(цв(f'- Error 🤦‍‍ - Done Selected: [{тм()}] - ok', с90))
    return тм()


def подготовить_онлайн() -> list[dict[str, str]]:
    мс = _сл()
    _ук(мс)
    os.environ['DARKIT_MODE'] = 'online'
    os.environ.setdefault('DARKIT_MODEL', _текущая_модель())
    return мс


def режим() -> str:
    return 'online'
    
# - By: T.me/sii_3