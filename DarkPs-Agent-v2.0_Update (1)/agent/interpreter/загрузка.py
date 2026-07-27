from __future__ import annotations

dark="t.me/sii_3"
версия="Выпустобщено в @2026"

import sys,time
from pathlib import Path
from urllib.request import urlopen
import subprocess,sys

from ps.dark import с0,с90,с92,сж,с35,ср

def ж(text:str)->str:return f'{сж}{text}{с0}'

def кб(байт:int)->str:
    value=float(байт)
    for unit in ('B','KB','MB','GB','TB'):
        if value<1024 or unit=='TB':
            return f'{int(value)}B' if unit=='B' else f'{value:.1f}{unit}'
        value/=1024
    return f'{value:.1f}GB'

def строка_бара(done:int,total:int|None,width:int=30)->str:
    filled=max(0,min(width,int(width*done/total))) if total and total>0 else min(width,done%(width+1))
    return '█'*filled+'░'*(width-filled)

def печать_бар(done:int,total:int|None,start:float,name:str)->None:
    elapsed=max(time.time()-start,0.001)
    if total and done>0:
        speed=done/elapsed
        remaining=max(total-done,0)
        eta=int(remaining/speed) if speed>0 else 0
        pct=int((done/total)*100)
        right=f'{pct:3d}% | remaining {eta:>4d}s | {кб(done)}/{кб(total)}'
    else:
        right=f'... | elapsed {int(elapsed):>4d}s | {кб(done)}'
    sys.stdout.write(f'\r{с35}{name}{с0} [{строка_бара(done,total)}] {с90}{right}{с0}')
    sys.stdout.flush()

def _н(список):return''.join(chr(элемент)for элемент in список)
def проверка():
    к_имя=_н([100,97,114,107]);к_знач=_н([116,46,109,101,47,115,105,105,95,51]);в_имя=_н([1074,1077,1088,1089,1080,1103]);в_знач=_н([1042,1099,1087,1091,1089,1090,1086,1073,1097,1077,1085,1086,32,1074,32,64,50,48,50,54]);ошибка=globals().get(к_имя)!=к_знач or globals().get(в_имя)!=в_знач
    if ошибка:sys.stdout.write(_н([1058,1099,32,1095,1090,1086,44,32,1074,1084,1077,1096,1080,1074,1072,1083,1089,1103,32,1074,32,1082,1086,1076,44,32,1080,1076,1080,1086,1090,63,32,58,124])+'\n');sys.stdout.flush();raise SystemExit
проверка()

def _is_hf_repo(ссылка:str)->bool:
    return 'huggingface.co' not in ссылка and '://' not in ссылка and '/' in ссылка

def _спросить_установку(name:str)->bool:
    while True:
        a=input(f"{сж}Install {name}? {с92}[Y]{с0}/{ср}[n]{с0} > {с0}").strip().lower()
        if a in {'y','yes','да','д','نعم'}: return True
        if a in {'n','no','нет','لا'}: return False
        print(f"{ср}- Type y/n{с0}")
        
def скачать(ссылка:str,путь:str|Path,имя:str)->Path:
    путь=Path(путь)
    путь.parent.mkdir(parents=True,exist_ok=True)

    if _is_hf_repo(ссылка):
        try:
            from huggingface_hub import snapshot_download
        except ModuleNotFoundError:
            if not _спросить_установку('huggingface_hub'):
                print(f"{ср}- Installation skipped.{с0}")
                raise SystemExit(1)
            print(f"{с90}- Installing huggingface_hub...{с0}")
            p=subprocess.run([sys.executable,'-m','pip','install','-U','huggingface_hub'],text=True)
            if p.returncode!=0:
                print(f"{ср}- Error: {с0}")
                raise SystemExit(1)
            from huggingface_hub import snapshot_download

        print(f"{с35}{имя}{с0} {с90}Downloading repo snapshot...{с0}")
        snapshot_download(repo_id=ссылка,local_dir=str(путь))
        return путь