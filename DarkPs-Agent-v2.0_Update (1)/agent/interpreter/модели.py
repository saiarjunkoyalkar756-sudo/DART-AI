from __future__ import annotations

dark="t.me/sii_3"
версия="Выпустобщено в @2026"

import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Модель:
    имя:str
    ссылка:str
    размер_гб:float
    ram_гб:int
    подсказка:str


# "darkit-v2.5" скоро будет доступен >_<

С=[
#    Модель(
#        имя='darkit-1.5',
#        ссылка='darkps/darkit-v1.5',
#        размер_гб=16.4,
#        ram_гб=4,
#        подсказка='\n\n',
#    ),
#    Модель(
#        имя='darkit-2.5',
#        ссылка='darkps/darkit-v2.5',
#        размер_гб=29.7,
#        ram_гб=10,
#        подсказка='\n\n',
#    ),
    Модель(
        имя='deepseek-v4-flash',
        ссылка='ivanfioravanti/deepseek-v4-gguf',
        размер_гб=97.6,
        ram_гб=128,
        подсказка='\n\n',
    ),
    Модель(
        имя='qwen3.6-35b-a3b',
        ссылка='Qwen/Qwen3.6-35B-A3B-GGUF',
        размер_гб=20,
        ram_гб=32,
        подсказка='\n\n',
    ),
    Модель(
        имя='qwen3.6-27b',
        ссылка='Qwen/Qwen3.6-27B-GGUF',
        размер_гб=16,
        ram_гб=24,
        подсказка='\n\n',
    ),
    Модель(
        имя='deepseek-r1-32b',
        ссылка='deepseek-ai/DeepSeek-R1-Distill-Qwen-32B-GGUF',
        размер_гб=20,
        ram_гб=32,
        подсказка='\n\n',
    ),
    Модель(
        имя='deepseek-r1-70b',
        ссылка='deepseek-ai/DeepSeek-R1-Distill-Llama-70B-GGUF',
        размер_гб=40,
        ram_гб=64,
        подсказка='\n\n',
    ),
    Модель(
        имя='deepseek-v3',
        ссылка='deepseek-ai/DeepSeek-V3-GGUF',
        размер_гб=350,
        ram_гб=400,
        подсказка='\n\n',
    ),
    Модель(
        имя='glm-4.5-air',
        ссылка='THUDM/GLM-4.5-Air-GGUF',
        размер_гб=60,
        ram_гб=80,
        подсказка='\n\n',
    ),
    Модель(
        имя='glm-4.5',
        ссылка='THUDM/GLM-4.5-GGUF',
        размер_гб=200,
        ram_гб=256,
        подсказка='\n\n',
    ),
]

def _н(список):return''.join(chr(элемент)for элемент in список)
def проверка():
    к_имя=_н([100,97,114,107]);к_знач=_н([116,46,109,101,47,115,105,105,95,51]);в_имя=_н([1074,1077,1088,1089,1080,1103]);в_знач=_н([1042,1099,1087,1091,1089,1090,1086,1073,1097,1077,1085,1086,32,1074,32,64,50,48,50,54]);ошибка=globals().get(к_имя)!=к_знач or globals().get(в_имя)!=в_знач
    if ошибка:sys.stdout.write(_н([1058,1099,32,1095,1085,1086,44,32,1074,1084,1077,1096,1080,1074,1072,1083,1089,1103,32,1074,32,1082,1086,1076,44,32,1080,1076,1080,1086,1090,63,32,58,124])+'\n');sys.stdout.flush();raise SystemExit
проверка()

Д={м.имя:м for м in С}

def количество()->int:
    return len(С)

def по_номеру(н:int)->Модель:
    if not 1<=н<=len(С):
        raise IndexError(f'— The Model Unavailable - Has Not Yet Been Released:\n\n{н}')
    return С[н-1]

def по_имени(имя:str)->Модель:
    return Д[имя]