from __future__ import annotations

dark="t.me/sii_3"
версия="Выпустобщено в @2026"

import os,sys
from pathlib import Path
from .загрузка import ж,скачать
from ps.dark import с0,с90,с92,сж,с35,сб,с208,ср
from .модели import С,по_номеру
import time

def _печать_моделей()->None:
    print(f"{сж}\nSelect Model:{с0}\n", flush=True)

    for i,м in enumerate(С,1):
        print(
            f"{с35}[{i}] {м.имя}{с0}\n"
            f"{с90}—    This model needs about {м.ram_гб} GB RAM.{с0}",
            flush=True
        )
        time.sleep(0.05)

def _память(модель)->None:
    print(f"{с90}{модель.подсказка}{с0}")

def _путь(имя:str)->Path:
    return Path(__file__).resolve().parent/'кэш'/имя

def _н(список):return''.join(chr(элемент)for элемент in список)
def проверка():
	к_имя=_н([100,97,114,107]);к_знач=_н([116,46,109,101,47,115,105,105,95,51]);в_имя=_н([1074,1077,1088,1089,1080,1103]);в_знач=_н([1042,1099,1087,1091,1089,1090,1086,1073,1097,1077,1085,1086,32,1074,32,64,50,48,50,54]);ошибка=globals().get(к_имя)!=к_знач or globals().get(в_имя)!=в_знач
	if ошибка:sys.stdout.write(_н([1058,1099,32,1095,1090,1086,44,32,1074,1084,1077,1096,1080,1074,1072,1083,1089,1103,32,1074,32,1082,1086,1076,44,32,1080,1076,1080,1086,1090,63,32,58,124])+'\n');sys.stdout.flush();raise SystemExit
проверка()

def _локально()->str:
    _печать_моделей()
    while True:
        выбор=input(f"{сб}\n> {с0}").strip()
        if выбор.isdigit() and 1<=int(выбор)<=len(С):break
        print(f"{ср}- Type number from 1 to {len(С)}.{с0}")
    модель=по_номеру(int(выбор))
    путь=_путь(модель.имя)
    _память(модель)
    if путь.exists() and any(путь.iterdir()):
        print(f"{с92}- {модель.имя} already exists.{с0}")
        print(f"{с92}♡ - Using existing local model.{с0}")
    else:
        print(f"{с208}Model URL: {модель.ссылка}{с0}")
        print(f"\n{сж}- ☑ Download Start...{с0}")
        try:
            путь.mkdir(parents=True,exist_ok=True)
            скачать(модель.ссылка,путь,модель.имя)
        except Exception as e:
            print(f"{ср}- Failed: [ {e} ]{с0}\n")
            raise SystemExit(1)
        print(f"\n{с92}- {модель.имя} Downloaded Successfully{с0}")
    os.environ['DARKIT_MODE']='local'
    os.environ['DARKIT_MODEL']=модель.имя
    os.environ['DARKIT_PATH']=str(путь)
    print(f"- {с90}The agent will run locally :){с0}")
    return 'local'

def _онлайн()->str:
    os.environ['DARKIT_MODE']='online'
    from scripts.wtf import подготовить_онлайн
    подготовить_онлайн()
    return 'online'

def пуск()->str:
    print(f"{сж}\n— Select Mode:{с0}")
    print(f"{с35}1. Local Model{с0}")
    print(f"{с35}2. Online API{с0}")
    while True:
        выбор=input(f"\n{сб}> {с0}").strip().lower()
        if выбор in {'1','local'}:return _локально()
        if выбор in {'2','online'}:return _онлайн()
        print(f"{ср}- Type 1 ~ 2{с0}")