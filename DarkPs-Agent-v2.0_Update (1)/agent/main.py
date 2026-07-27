# - @2026 | Version 2.0
# - Created By: T.me/sii_3
# - Mr Dark

# ~ Agent DarkPs Official [>_]

from __future__ import annotations

dark="t.me/sii_3"
версия="Выпустобщено в @2026"

скорость = 0.0005 # Logo Print Speed :|

from ps.dark import *
from interpreter import пуск as интер_пуск
import asyncio,re
import sys

# вы можете добавить свой собственныи логотип поддерживаются разные цвета просто скопируите и вставьте. 👍

with open("логотип.md", "r", encoding="utf-8") as f:
    л = f.read()

ят = True

def цв(ц):
    ц = ц.lstrip("#")
    р, г, б = int(ц[0:2], 16), int(ц[2:4], 16), int(ц[4:6], 16)
    return f"\033[38;2;{р};{г};{б}m"

def чист(т):
    т = re.sub(r"<[^>]+>", "", т)
    т = re.sub(r"\[/?(font|size)[^\]]*\]", "", т)
    return т
def _н(список):return''.join(chr(элемент)for элемент in список)
def проверка():
	к_имя=_н([100,97,114,107]);к_знач=_н([116,46,109,101,47,115,105,105,95,51]);в_имя=_н([1074,1077,1088,1089,1080,1103]);в_знач=_н([1042,1099,1087,1091,1089,1090,1086,1073,1097,1077,1085,1086,32,1074,32,64,50,48,50,54]);ошибка=globals().get(к_имя)!=к_знач or globals().get(в_имя)!=в_знач
	if ошибка:sys.stdout.write(_н([1058,1099,32,1095,1090,1086,44,32,1074,1084,1077,1096,1080,1074,1072,1083,1089,1103,32,1074,32,1082,1086,1076,44,32,1080,1076,1080,1086,1090,63,32,58,124])+'\n');sys.stdout.flush();raise SystemExit
проверка()
async def д():
    ч = чист(л)
    ш = re.compile(r"#[0-9a-fA-F]{6}")

    тц = ""

    for стр in ч.splitlines():
        п = 0

        for м in ш.finditer(стр):
            н, к = м.span()

            for ch in стр[п:н]:
                if ят and тц:
                    print(f"{цв(тц)}{ch}\033[0m", end="", flush=True)
                else:
                    print(ch, end="", flush=True)
                await asyncio.sleep(скорость)

            тц = м.group()
            п = к

        for ch in стр[п:]:
            if ят and тц:
                print(f"{цв(тц)}{ch}\033[0m", end="", flush=True)
            else:
                print(ch, end="", flush=True)
            await asyncio.sleep(скорость)

        print()
    
if __name__ == '__main__':
    asyncio.run(д())

    from ps.серв import бан
    бан()

    интер_пуск()
    глв()
    
# - By: T.me/sii_3