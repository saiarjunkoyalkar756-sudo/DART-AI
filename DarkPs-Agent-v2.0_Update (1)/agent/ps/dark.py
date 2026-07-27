# - @2026 | Version 2.0
# - Created By: T.me/sii_3
# - Mr Dark

# ~ Agent DarkPs Official [>_]

from __future__ import annotations

dark='t.me/sii_3'
версия='Выпустобщено в @2026'


_Ah='CONTINUE:'
_Ag='parameters'
_Af='description'
_Ae='_mcp_server'
_Ad='2024-11-05'
_Ac='clientInfo'
_Ab='capabilities'
_Aa='protocolVersion'
_AZ='План не найден'
_AY='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
_AX='User-Agent'
_AW='think'
_AV='steps'
_AU='target'
_AT='архив'
_AS='params'
_AR='method'
_AQ='jsonrpc'
_AP='Projects'
_AO='безоп'
_AN='контекст'
_AM='(пусто)'
_AL='мысль'
_AK='PROGRESS:'
_AJ='FINAL:'
_AI='TOOL:'
_AH='дум_показано'
_AG='дум_полн'
_AF='file'
_AE='path'
_AD='навык'
_AC='поиск_веб'
_AB='замена'
_AA='github_репо'
_A9='github_поиск'
_A8='arguments'
_A7='тэги'
_A6='bing'
_A5='заметки'
_A4='статус'
_A3='NO_COLOR'
_A2='нач'
_A1='\n\n'
_A0='вопрос'
_z='удаление'
_y='очистка'
_x='запись'
_w='список'
_v='чтение'
_u='mcp'
_t='tool'
_s='github_чтение'
_r='command'
_q='одобр'
_p='текст'
_o='готово'
_n='план'
_m='error'
_l='сод'
_k='двиг'
_j='при'
_i='ddg'
_h='.darkps'
_g='continue'
_f='нл'
_e='установка'
_d='поиск'
_c='replace'
_b='ключ'
_a='цель'
_Z='ожд'
_Y='final'
_X='финал'
_W='text'
_V='время'
_U='рез'
_T='шаги'
_S='блок_бф'
_R='инс_бф'
_Q='шелл'
_P='system'
_O='assistant'
_N='name'
_M='запрос'
_L='вкл'
_K='успех'
_J='default'
_I='id'
_H='реж'
_G='utf-8'
_F='role'
_E='content'
_D='\n'
_C=False
_B=None
_A=True

import json,os,random,shutil,string,sys,zipfile,tarfile,threading,queue,time,urllib.parse,urllib.request,re,subprocess,base64,requests,hashlib,datetime,sqlite3,traceback,textwrap
from pathlib import Path
from typing import Any,Callable,Dict,List,Optional,Tuple,Union
from dataclasses import dataclass,field,asdict
from enum import Enum,auto
from collections import deque,defaultdict
sys.path.append('/')
sys.path.append(str(Path(__file__).resolve().parent))
try:
    from scripts.wtf import вм,по,рг,зг
except Exception:
    def вм():
        return None
    def по(*args, **kwargs):
        return []
    def рг(*args, **kwargs):
        return (None, None)
    def зг(*args, **kwargs):
        return {'User-Agent': 'Mozilla/5.0'}
try:
    from interpreter.github import гт,сгт,пгт,угт,гп,гр,гс
except Exception:
    def _noop(*args, **kwargs):
        return None
    гт = сгт = пгт = угт = гп = гр = гс = _noop
try:
    from interpreter.duckduck import поиск_ддг
except Exception:
    def поиск_ддг(*args, **kwargs):
        return []
try:
    from interpreter.bing import поиск_бинг
except Exception:
    def поиск_бинг(*args, **kwargs):
        return []
try:
    from interpreter.brave import поиск_брейв
except Exception:
    def поиск_брейв(*args, **kwargs):
        return []
try:
    from interpreter.serp import поиск_серп
except Exception:
    def поиск_серп(*args, **kwargs):
        return []
try:
    from interpreter.google_search import поиск_гугл
except Exception:
    def поиск_гугл(*args, **kwargs):
        return []
с0='\x1b[0m'
с2='\x1b[2m'
с1='\x1b[1m'
ср='\x1b[31m'
сз='\x1b[32m'
сж='\x1b[33m'
сс='\x1b[34m'
сг='\x1b[36m'
сб='\x1b[37m'
с90='\x1b[90m'
с250='\x1b[38;5;250m'
с92='\x1b[92m'
с96='\x1b[96m'
с35='\x1b[35m'
с208='\x1b[38;5;208m'
с118='\x1b[38;5;118m'
с51='\x1b[38;5;51m'
с153='\x1b[38;5;153m'
фон_код='\x1b[48;5;236m'
фон_вывод='\x1b[48;5;24m'
def цв(т,ц=сб,*,ж=_C,тм=_C):
    if os.getenv(_A3)or not sys.stdout.isatty():return т
    ч=[]
    if ж:ч.append(с1)
    if тм:ч.append(с2)
    ч.append(ц);return''.join(ч)+т+с0
_тег_цвет=re.compile('\\{\\{ц:(\\d{1,3}(?:;\\d{1,3})?)(,ж)?\\}\\}(.*?)\\{\\{/ц\\}\\}',re.DOTALL)
_тег_жирн=re.compile('\\{\\{ж\\}\\}(.*?)\\{\\{/ж\\}\\}',re.DOTALL)
def стиль(т):
    if os.getenv(_A3)or not sys.stdout.isatty():т=_тег_цвет.sub(lambda m:m.group(3),т);т=_тег_жирн.sub(lambda m:m.group(1),т);return т
    def _зц(m):код,жфл,внутр=m.group(1),m.group(2),m.group(3);префикс=с1 if жфл else'';return f"[38;5;{код}m{префикс}{внутр}{с0}"
    т=_тег_цвет.sub(_зц,т);т=_тег_жирн.sub(lambda m:f"{с1}{m.group(1)}{с0}",т);return т
_ключ_слова={'def','class','return','if','elif','else','for','while','try','except','finally','import','from','as','with','pass','break',_g,'yield','lambda','global','nonlocal','raise','assert','async','await','in','is','not','and','or','None','True','False','const','let','var','function','export',_J,'new','this','public','private','static','void','int','string','bool','null','struct','enum','interface','type','switch','case','do'}
_подсв_строка=re.compile('(\'(?:[^\'\\\\]|\\\\.)*\'|\\"(?:[^\\"\\\\]|\\\\.)*\\")')
_подсв_коммент=re.compile('(#.*$|//.*$)')
_подсв_число=re.compile('\\b(\\d+\\.?\\d*)\\b')
_подсв_слово=re.compile('\\b([A-Za-zА-Яа-яЁё_][A-Za-zА-Яа-яЁё0-9_]*)\\b')
def _подсветка_строки(строка):
    if os.getenv(_A3)or not sys.stdout.isatty():return строка
    части=_подсв_строка.split(строка);вых=[];комм_найден=_C
    for(i,часть)in enumerate(части):
        if комм_найден:вых.append(f"[38;5;242m{часть}[0m");continue
        if i%2==1:вых.append(f"[38;5;150m{часть}[0m");continue
        комм=_подсв_коммент.search(часть);хвост=''
        if комм:хвост=часть[комм.start():];часть=часть[:комм.start()];комм_найден=_A
        часть2=_подсв_число.sub(lambda m:f"[38;5;180m{m.group(1)}[0m",часть)
        def _слово(m):
            с=m.group(1)
            if с in _ключ_слова:return f"[38;5;213m{с}[0m"
            return с
        часть2=_подсв_слово.sub(_слово,часть2);вых.append(часть2)
        if хвост:вых.append(f"[38;5;242m{хвост}[0m")
    итог=''.join(вых);return итог
_АНСИ_ОЧИСТ=re.compile('\\033\\[[0-9;]*m')
def пузырь(текст,*,фон=фон_код,подсветка=_A,метка=''):
    A='─';если_тти=not(os.getenv(_A3)or not sys.stdout.isatty());строки=текст.rstrip(_D).split(_D)or[''];шир=min(100,max((len(с)for с in строки),default=0)+4);шир=max(шир,len(метка)+6,8);низ='╰'+A*(шир-2)+'╯'
    if метка:м=f" {метка} ";верх='╭─'+м+A*max(0,шир-4-len(м))+'╮'
    else:верх='╭'+A*(шир-2)+'╮'
    итог=[];итог.append(цв(верх,с90,тм=_A)if если_тти else верх)
    for стр in строки:
        стр_показ=_подсветка_строки(стр)if подсветка else стр;видим_длина=len(_АНСИ_ОЧИСТ.sub('',стр_показ));отступ=' '*max(0,шир-4-видим_длина)
        if если_тти:итог.append(f"{цв("│",с90,тм=_A)} {фон}{стр_показ}{отступ}{с0} {цв("│",с90,тм=_A)}")
        else:итог.append(f"│ {стр}{" "*max(0,шир-4-len(стр))} │")
    итог.append(цв(низ,с90,тм=_A)if если_тти else низ);return _D.join(итог)
class Инд:
    кр=['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏']
    def __init__(и):и._а=_C;и._п=_B;и._с='';и._и=0
    def ст(и,с='Думаю'):и._с=с;и._а=_A;и._и=0;и._п=threading.Thread(target=и._ц,daemon=_A);и._п.start()
    def _ц(и):
        while и._а:к=и.кр[и._и%len(и.кр)];print(f"\r{цв(к,с51)} {цв(и._с,с90)}",end='',flush=_A);и._и+=1;time.sleep(.08)
    def об(и,с):и._с=с
    def стп(и,ф=_B):
        и._а=_C
        if и._п:и._п.join(timeout=.5)
        print('\r'+' '*(len(и._с)+10)+'\r',end='')
        if ф:print(цв(ф,сз))
    def шк(и,т,в,п='',д=30):
        if в==0:return
        з=int(д*т//в);ш='█'*з+'░'*(д-з);пц=т/в*100;ц=сз if пц>70 else сж if пц>30 else ср;print(f"\r{цв(п,сс)} [{цв(ш,ц)}] {цв(f"{пц:.1f}%",с1)} ({т}/{в})",end='',flush=_A)
инд=Инд()
class Вп:
    def __init__(вп,п=_B):вп.п=п or Path.home()/_h/'memory.db';вп.п.parent.mkdir(parents=_A,exist_ok=_A);вп._и();вп._к={};вп._д=defaultdict(int)
    def _и(вп):б=sqlite3.connect(str(вп.п));к=б.cursor();к.execute('\n            CREATE TABLE IF NOT EXISTS кф (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                путь TEXT NOT NULL, содержимое TEXT NOT NULL,\n                язык TEXT, резюме TEXT, токены INTEGER DEFAULT 0,\n                создан REAL NOT NULL, доступ REAL, счётчик INTEGER DEFAULT 0,\n                сессия TEXT\n            )\n        ');к.execute('\n            CREATE TABLE IF NOT EXISTS рв (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                инструмент TEXT NOT NULL, вход TEXT,\n                результат TEXT NOT NULL, успех BOOLEAN,\n                время REAL, создан REAL NOT NULL, сессия TEXT\n            )\n        ');к.execute('\n            CREATE TABLE IF NOT EXISTS чк (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                роль TEXT NOT NULL, содержимое TEXT NOT NULL,\n                резюме TEXT, важность REAL DEFAULT 0.5,\n                создан REAL NOT NULL, сессия TEXT, индекс INTEGER\n            )\n        ');к.execute('\n            CREATE TABLE IF NOT EXISTS пр (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                запрос TEXT NOT NULL, движок TEXT,\n                результаты TEXT, количество INTEGER,\n                создан REAL NOT NULL, сессия TEXT\n            )\n        ');к.execute('\n            CREATE TABLE IF NOT EXISTS рз (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                тема TEXT NOT NULL, резюме TEXT NOT NULL,\n                тип TEXT, создан REAL NOT NULL, обновлён REAL\n            )\n        ');к.execute("\n            CREATE TABLE IF NOT EXISTS планы_пр (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                проект TEXT NOT NULL,\n                цель TEXT NOT NULL,\n                шаги TEXT NOT NULL,\n                статус TEXT DEFAULT 'активен',\n                заметки TEXT DEFAULT '',\n                создан REAL NOT NULL, обновлён REAL NOT NULL\n            )\n        ");б.commit();б.close()
    def кс(вп,путь,сод,яз='',рз='',сс=_J):кл=hashlib.md5(f"{путь}:{сод[:100]}".encode()).hexdigest()[:16];тк=len(сод)//4;б=sqlite3.connect(str(вп.п));к=б.cursor();к.execute('\n            INSERT OR REPLACE INTO кф \n            (путь, содержимое, язык, резюме, токены, создан, доступ, сессия)\n            VALUES (?, ?, ?, ?, ?, ?, ?, ?)\n        ',(путь,сод,яз,рз,тк,time.time(),time.time(),сс));б.commit();б.close();вп._к[кл]={'т':'код','п':путь,'с':сод};return кл
    def пк(вп,путь,сс=_J):
        б=sqlite3.connect(str(вп.п));к=б.cursor();к.execute('\n            SELECT путь, содержимое, язык, резюме, токены \n            FROM кф WHERE путь = ? AND сессия = ?\n            ORDER BY создан DESC LIMIT 1\n        ',(путь,сс));р=к.fetchone()
        if р:к.execute('\n                UPDATE кф SET счётчик = счётчик + 1, доступ = ?\n                WHERE путь = ? AND сессия = ?\n            ',(time.time(),путь,сс));б.commit()
        б.close()
        if р:return{'путь':р[0],'содержимое':р[1],'язык':р[2],'резюме':р[3],'токены':р[4]}
    def зр(вп,и,вх,рз,у,вр,сс=_J):кл=f"рв_{hashlib.md5(f"{и}:{time.time()}".encode()).hexdigest()[:12]}";б=sqlite3.connect(str(вп.п));к=б.cursor();к.execute('\n            INSERT INTO рв (инструмент, вход, результат, успех, время, создан, сессия)\n            VALUES (?, ?, ?, ?, ?, ?, ?)\n        ',(и,json.dumps(вх),рз,у,вр,time.time(),сс));б.commit();б.close();return кл
    def пп(тхт):
        if not тхт or not isinstance(тхт,str):return _B,_B,_B
        tool_idx=тхт.find(_AI)
        if tool_idx!=-1:
            json_start=tool_idx+5
            while json_start<len(тхт)and тхт[json_start].isspace():json_start+=1
            if json_start<len(тхт)and тхт[json_start]=='{':
                brace_count=0;in_string=_C;escape=_C
                for i in range(json_start,len(тхт)):
                    ch=тхт[i]
                    if escape:escape=_C;continue
                    if ch=='\\':escape=_A;continue
                    if ch=='"'and not escape:in_string=not in_string;continue
                    if not in_string:
                        if ch=='{':brace_count+=1
                        elif ch=='}':
                            brace_count-=1
                            if brace_count==0:
                                try:tool_json=json.loads(тхт[json_start:i+1]);return tool_json,_B,_B
                                except json.JSONDecodeError:pass
                                break
        final_idx=тхт.find(_AJ)
        if final_idx!=-1:return _B,тхт[final_idx+6:].strip(),_B
        prog_idx=тхт.find(_AK)
        if prog_idx!=-1:return _B,_B,тхт[prog_idx+9:].strip()
        return _B,_B,_B
    def ок(вп,сс=_J,мт=8000):
        б=sqlite3.connect(str(вп.п));к=б.cursor();к.execute('\n            SELECT путь, резюме, токены FROM кф\n            WHERE сессия = ? ORDER BY счётчик DESC, доступ DESC LIMIT 20\n        ',(сс,));ф=к.fetchall();к.execute('\n            SELECT инструмент, результат FROM рв\n            WHERE сессия = ? ORDER BY создан DESC LIMIT 10\n        ',(сс,));в=к.fetchall();б.close();ст=['=== EXTERNAL MEMORY ===\n']
        if ф:
            ст.append('[FILES]')
            for f in ф:ст.append(f"  📄 {f[0]} ({f[1]or"No summary"} | ~{f[2]} токенов)")
            ст.append('')
        if в:
            ст.append('[RUNS]')
            for v in в:п=v[1][:100].replace(_D,' ');ст.append(f"  🔧 {v[0]}: {п}...")
            ст.append('')
        кт=_D.join(ст)
        if len(кт)>мт*4:ст=ст[:len(ст)//2];ст.append('\n... (сокращено)');кт=_D.join(ст)
        return кт
    def зп(вп,з,д,р,сс=_J):б=sqlite3.connect(str(вп.п));к=б.cursor();к.execute('\n            INSERT INTO пр (запрос, движок, результаты, количество, создан, сессия)\n            VALUES (?, ?, ?, ?, ?, ?)\n        ',(з,д,json.dumps(р),len(р),time.time(),сс));б.commit();б.close();return f"п_{int(time.time())}"
    def ип(вп,з,сс=_J):
        б=sqlite3.connect(str(вп.п));к=б.cursor();к.execute('\n            SELECT движок, результаты, количество, создан FROM пр\n            WHERE запрос LIKE ? AND сессия = ? ORDER BY создан DESC LIMIT 1\n        ',(f"%{з}%",сс));р=к.fetchone();б.close()
        if р:return{'движок':р[0],'результаты':json.loads(р[1]),'количество':р[2],'возраст_ч':(time.time()-р[3])/3600}
    def сохр_план(вп,проект,цель,шаги,заметки=''):б=sqlite3.connect(str(вп.п));к=б.cursor();к.execute("\n            INSERT INTO планы_пр (проект, цель, шаги, статус, заметки, создан, обновлён)\n            VALUES (?, ?, ?, 'активен', ?, ?, ?)\n        ",(проект,цель,json.dumps(шаги,ensure_ascii=_C),заметки,time.time(),time.time()));ид=к.lastrowid;б.commit();б.close();return ид
    def план_проекта(вп,проект):
        б=sqlite3.connect(str(вп.п));к=б.cursor();к.execute("\n            SELECT id, цель, шаги, статус, заметки, создан, обновлён FROM планы_пр\n            WHERE проект = ? AND статус = 'активен' ORDER BY обновлён DESC LIMIT 1\n        ",(проект,));р=к.fetchone();б.close()
        if not р:return
        return{_I:р[0],_a:р[1],_T:json.loads(р[2]),_A4:р[3],_A5:р[4],'создан':р[5],'обновлён':р[6]}
    def обн_план(вп,ид,шаги,заметки=_B):
        б=sqlite3.connect(str(вп.п));к=б.cursor()
        if заметки is not _B:к.execute('UPDATE планы_пр SET шаги = ?, заметки = ?, обновлён = ? WHERE id = ?',(json.dumps(шаги,ensure_ascii=_C),заметки,time.time(),ид))
        else:к.execute('UPDATE планы_пр SET шаги = ?, обновлён = ? WHERE id = ?',(json.dumps(шаги,ensure_ascii=_C),time.time(),ид))
        б.commit();б.close()
    def завершить_план(вп,ид):б=sqlite3.connect(str(вп.п));к=б.cursor();к.execute("UPDATE планы_пр SET статус = 'готово', обновлён = ? WHERE id = ?",(time.time(),ид));б.commit();б.close()
class Поиск:
    дв={_i:{_L:_A,_j:1,_b:_C},_A6:{_L:_A,_j:2,_b:_C},'brave':{_L:_C,_j:3,_b:_A,'env':'BRAVE_API_KEY'},'serp':{_L:_C,_j:4,_b:_A,'env':'SERPAPI_KEY'},'google':{_L:_C,_j:5,_b:_A,'env':'GOOGLE_API_KEY'}}
    def __init__(п):п._с=requests.Session();п._с.headers.update({_AX:_AY,'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'en-US,en;q=0.5'});п._по=_B;п._сч=defaultdict(int)
    def ищи(п,з,ог=10):
        ош=[]
        if п.дв[_i][_L]:
            try:
                инд.ст('Поиск DuckDuckGo...');р=поиск_ддг(п._с,з,ог);инд.стп()
                if р:п._сч[_i]+=1;return{_K:_A,_k:_i,_U:р,_M:з}
            except Exception as e:инд.стп();ош.append(f"DDG: {e}");п.дв[_i][_L]=_C
        if п.дв[_A6][_L]:
            try:
                инд.ст('Поиск Bing...');р=поиск_бинг(п._с,з,ог);инд.стп()
                if р:п._сч[_A6]+=1;return{_K:_A,_k:_A6,_U:р,_M:з}
            except Exception as e:инд.стп();ош.append(f"Bing: {e}")
        for(дн,кф)in п.дв.items():
            if not кф[_L]or not кф[_b]:continue
            кл=os.getenv(кф['env'])
            if not кл:continue
            try:
                инд.ст(f"Поиск {дн}...")
                if дн=='brave':р=поиск_брейв(п._с,з,кл,ог)
                elif дн=='serp':р=поиск_серп(п._с,з,кл,ог)
                elif дн=='google':р=поиск_гугл(п._с,з,кл,ог)
                инд.стп()
                if р:п._сч[дн]+=1;return{_K:_A,_k:дн,_U:р,_M:з}
            except Exception as e:инд.стп();ош.append(f"{дн}: {e}")
        return{_K:_C,_k:_B,_U:[],_M:з,'ошибки':ош,'сообщ':'Все движки поиска недоступны. Проверьте интернет или API ключи.'}
    def ст(п):
        ст=['=== SEARCH STATISTICS ===']
        for(д,с)in sorted(п._сч.items(),key=lambda x:x[1],reverse=_A):ст.append(f"  ☑ {д}: {с} успешных")
        return _D.join(ст)
# - By: T.me/sii_3
def зк(кр, отн):
    п = Path(str(отн)).expanduser()
    if not п.is_absolute():
        п = (Path(кр) / п).resolve()
    else:
        п = п.resolve()

    кр = Path(кр).resolve()
    if п != кр and кр not in п.parents:
        raise ValueError(f"Path escapes project root: {отн}")

    return п
class Пф:
    рм=2000;мр=50000
    def __init__(п,р):п.р=р;п._о={}
    def пиши(п,путь,сод,шк=_A):
        ц=зк(п.р, путь);ц.parent.mkdir(parents=_A,exist_ok=_A)
        if len(сод)<п.мр:ц.write_text(сод,encoding=_G);return f"☑ Written: {путь} ({len(сод)} симв)"
        return п._ч(путь,сод,шк)
    def _ч(п,путь,сод,шк):
        A='Запись';ч=п._р(сод);вс=len(ч)
        if шк:print(цв(f"\n📄 Large file: {путь}",сс,ж=_A));print(цв(f"   Size: {len(сод)} chars | Parts: {вс}\n",с90))
        ц=зк(п.р, путь);ц.parent.mkdir(parents=_A,exist_ok=_A)
        with open(ц,'w',encoding=_G)as ф:ф.write(ч[0]);ф.flush()
        if шк:инд.шк(1,вс,A,30)
        for(i,чс)in enumerate(ч[1:],2):
            with open(ц,'a',encoding=_G)as ф:ф.write(чс);ф.flush()
            if шк:инд.шк(i,вс,A,30)
            time.sleep(.05)
        if ц.exists():
            actual=ц.stat().st_size
            expected=len(сод.encode(_G))
            if actual<expected*0.9:
                return f"☒ Write incomplete: {actual}/{expected} bytes"
        if шк:print(цв(f"\n☑ Done: {путь}",сз,ж=_A))
        return f"☑ Written: {путь} ({len(сод)} симв, {вс} частей)"
    def _р(п,сод):
        РМ_БЕЗОП=800
        ст=сод.split(_D);ч=[];тч=[];тр=0
        for с in ст:
            рс=len(с)+1
            if тр+рс>РМ_БЕЗОП and тч:ч.append(_D.join(тч)+_D);тч=[с];тр=рс
            else:тч.append(с);тр+=рс
        if тч:ч.append(_D.join(тч))
        return ч if ч else[сод]
    def доб(п,путь,сод):
        ц=зк(п.р, путь);ц.parent.mkdir(parents=_A,exist_ok=_A)
        with open(ц,'a',encoding=_G)as ф:ф.write(сод)
        return f"☑ Appended: {путь}"
    def зм(п,путь,н,з):
        ц=зк(п.р, путь)
        if not ц.exists():return f"☒ No file: {путь}"
        с=ц.read_text(encoding=_G)
        if н not in с:return f"☒ Текст не найден: {путь}"
        ц.write_text(с.replace(н,з),encoding=_G);return f"☑ Modified: {путь}"
class УР(Enum):СРОЧ=auto();ФОН=auto();РАБ=auto();ДОЛГ=auto()
@dataclass
class Мысль:сод:str;ур:УР;вр:float=field(default_factory=time.time);ув:float=1.;ист:str='рассуждение';тэги:List[str]=field(default_factory=list)
class Разум:
    def __init__(р,п=_B,вп=_B):р.п=п or Path.home()/_h/'mind.db';р.п.parent.mkdir(parents=_A,exist_ok=_A);р.вп=вп;р._и();р.оп=deque(maxlen=50);р._фп=_B;р._фо=queue.Queue();р._фа=_C;р._дк={};р._зд()
    def _и(р):б=sqlite3.connect(str(р.п));к=б.cursor();к.execute("\n            CREATE TABLE IF NOT EXISTS мысли (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                содержимое TEXT NOT NULL, уровень TEXT NOT NULL,\n                время REAL NOT NULL, уверенность REAL DEFAULT 1.0,\n                источник TEXT DEFAULT 'рассуждение', тэги TEXT DEFAULT '[]',\n                сессия TEXT\n            )\n        ");к.execute('\n            CREATE TABLE IF NOT EXISTS опыт (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                тип TEXT NOT NULL, вход TEXT,\n                результат TEXT, успех REAL, уроки TEXT,\n                время REAL NOT NULL, частота INTEGER DEFAULT 1\n            )\n        ');к.execute("\n            CREATE TABLE IF NOT EXISTS профили (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                пользователь TEXT UNIQUE, предпочтения TEXT DEFAULT '{}',\n                счётчик INTEGER DEFAULT 0,\n                стиль TEXT DEFAULT '{}',\n                создан REAL, обновлён REAL\n            )\n        ");б.commit();б.close()
    def _зд(р):
        try:
            б=sqlite3.connect(str(р.п));к=б.cursor();к.execute("SELECT содержимое, уверенность, тэги FROM мысли WHERE уровень='ДОЛГ' ORDER BY время DESC LIMIT 100")
            for row in к.fetchall():кл=hashlib.md5(row[0].encode()).hexdigest()[:16];р._дк[кл]={_l:row[0],'ув':row[1],_A7:json.loads(row[2])if row[2]else[]}
            б.close()
        except Exception:pass
    def думай(р,сод,ур=УР.СРОЧ,ув=1.,тэги=_B):
        м=Мысль(сод=сод,ур=ур,ув=ув,тэги=тэги or[])
        if ур==УР.СРОЧ:р.оп.append(м);р._см(м)
        elif ур==УР.ФОН:
            р._фо.put(м)
            if not р._фа:р._нф()
        elif ур==УР.РАБ:р.оп.append(м);р._см(м)
        elif ур==УР.ДОЛГ:р._здм(м)
        return м
    def _см(р,м,сс=_J):
        try:б=sqlite3.connect(str(р.п));к=б.cursor();к.execute('INSERT INTO мысли (содержимое, уровень, время, уверенность, источник, тэги, сессия) VALUES (?, ?, ?, ?, ?, ?, ?)',(м.сод,м.ур.name,м.вр,м.ув,м.ист,json.dumps(м.тэги),сс));б.commit();б.close()
        except Exception:pass
    def _здм(р,м):кл=hashlib.md5(м.сод.encode()).hexdigest()[:16];р._дк[кл]={_l:м.сод,'ув':м.ув,_A7:м.тэги};р._см(м)
    def _нф(р):р._фа=_A;р._фп=threading.Thread(target=р._фц,daemon=_A);р._фп.start()
    def _фц(р):
        while р._фа:
            try:
                м=р._фо.get(timeout=5);а=р._ам(м)
                if а['важ']>.7:р.оп.append(а[_AL])
                р._см(а[_AL])
            except queue.Empty:continue
            except Exception:continue
    def _ам(р,м):
        в=м.ув;бт={'критично',_m,'безопасность',_M,'код','файл'}
        if any(т in бт for т in м.тэги):в=min(1.,в+.3)
        return{_AL:м,'важ':в}
    def вспомни(р,з,ог=10):
        р=[];зн=з.lower()
        for м in р.оп:
            if зн in м.сод.lower()or any(зн in т.lower()for т in м.тэги):р.append(м)
        for(кл,д)in р._дк.items():
            if зн in д[_l].lower()or any(зн in т.lower()for т in д[_A7]):р.append(Мысль(сод=д[_l],ур=УР.ДОЛГ,ув=д['ув'],тэги=д[_A7]))
        р.sort(key=lambda x:x.ув,reverse=_A);return р[:ог]
    def оп_сумм(р):
        if not р.оп:return _AM
        return _D.join([f"[{м.ур.name}] {м.сод[:100]}..."for м in list(р.оп)[-10:]])
    def стп_ф(р):
        р._фа=_C
        if р._фп and р._фп.is_alive():р._фп.join(timeout=2)
class ТП(Enum):СТРАТ=auto();ТАКТ=auto();ИСП=auto();РЕЗ=auto()
@dataclass
class Шаг:id:str;оп:str;дей:str;пар:Dict[str,Any]=field(default_factory=dict);зав:List[str]=field(default_factory=list);ст:str='ожид';рез:Optional[str]=_B;вр:float=.0;пв:int=0;мп:int=3
@dataclass
class План:id:str;т:ТП;ц:str;ш:List[Шаг]=field(default_factory=list);созд:float=field(default_factory=time.time);зав:Optional[float]=_B;усп:Optional[bool]=_B;рез:Optional['План']=_B
class Планир:
    def __init__(п,р):п.р=р;п.ап={};п.и=deque(maxlen=100);п._с=0
    def созд(п,ц,т=ТП.ТАКТ,кт=_B):
        п._с+=1;ид=f"план_{п._с}_{сл(4)}";пл=План(id=ид,т=т,ц=ц)
        if т==ТП.СТРАТ:пл.ш=п._сш(ц,кт)
        elif т==ТП.ТАКТ:пл.ш=п._тш(ц,кт)
        elif т==ТП.ИСП:пл.ш=п._иш(ц,кт)
        else:пл.ш=п._рш(ц,кт)
        if т in(ТП.СТРАТ,ТП.ТАКТ):пл.рез=п._срп(пл)
        п.ап[ид]=пл;п.р.думай(f"Создан {т.name} план '{ид}' для: {ц}",УР.РАБ,тэги=[_n,т.name.lower()]);return пл
    def _сш(п,ц,кт):return[Шаг(id='с1',оп='Анализ ситуации',дей='анализ',пар={_a:ц}),Шаг(id='с2',оп='Определить цели',дей='цели',зав=['с1'],пар={_AN:кт}),Шаг(id='с3',оп='Метрики успеха',дей='метрики',зав=['с2']),Шаг(id='с4',оп='Распределить ресурсы',дей='ресурсы',зав=['с3']),Шаг(id='с5',оп='Мониторинг',дей='монитор',зав=['с4'])]
    def _тш(п,ц,кт):return[Шаг(id='т1',оп='Разбить задачи',дей='разбить',пар={_a:ц}),Шаг(id='т2',оп='Приоритеты',дей='приор',зав=['т1']),Шаг(id='т3',оп='Выполнить основную',дей='выполн',зав=['т2']),Шаг(id='т4',оп='Проверить',дей='провер',зав=['т3']),Шаг(id='т5',оп='Отчёт',дей='отчёт',зав=['т4'])]
    def _иш(п,ц,кт):return[Шаг(id='и1',оп=f"Выполнить: {ц}",дей='выполн',пар={'срочно':_A}),Шаг(id='и2',оп='Проверить выполнение',дей='провер',зав=['и1'])]
    def _рш(п,ц,кт):return[Шаг(id='р1',оп='Оценить точку отказа',дей='оценка'),Шаг(id='р2',оп='Альтернатива',дей='альт',зав=['р1']),Шаг(id='р3',оп='Эскалация',дей='эскал',зав=['р2'])]
    def _срп(п,пл):return План(id=f"{пл.id}_рез",т=ТП.РЕЗ,ц=f"Резерв: {пл.ц}",ш=п._рш(пл.ц,{}))
    def выполни(п,ид,и):
        A='выполнение';пл=п.ап.get(ид)
        if not пл:return{_K:_C,_m:_AZ}
        вс=[];пш=[]
        for ш in пл.ш:
            if ш.ст==_o:вс.append(ш);continue
            зу=all(any(s.id==з and s.ст==_o for s in пл.ш)for з in ш.зав)
            if not зу:пш.append((ш,'Зависимости не выполнены'));continue
            try:ш.ст='актив';р=и(ш);ш.рез=р;ш.ст=_o;вс.append(ш);п.р.думай(f"Шаг {ш.id} готов",УР.РАБ,тэги=[A,_K])
            except Exception as e:
                ш.ст=_m;ш.пв+=1
                if ш.пв<ш.мп:ш.ст='ожид';п.р.думай(f"Повтор {ш.id} (попытка {ш.пв+1})",УР.ФОН,тэги=['повтор',A])
                else:
                    пш.append((ш,str(e)))
                    if пл.рез:п.р.думай(f"Активирован резерв {ид}",УР.РАБ,тэги=['резерв','тревога'])
        пл.зав=time.time();пл.усп=len(пш)==0;п.и.append(пл);return{_K:пл.усп,_o:len(вс),'ошибки':len(пш),_n:пл}
    def ст_пл(п,ид):
        пл=п.ап.get(ид)
        if not пл:return _AZ
        ст=[f"План: {пл.ц} ({пл.т.name})"];ст.append(f"Status: {"Готово"if пл.усп else"Активен"if пл.усп is _B else"Error"}");ст.append('Шаги:')
        for ш in пл.ш:ик='+'if ш.ст==_o else'>'if ш.ст=='актив'else'о';ст.append(f"  {ик} {ш.id}: {ш.оп} [{ш.ст}]")
        return _D.join(ст)
class ТК(Enum):ВРЕМ=auto();ПРОС=auto();ЭМОЦ=auto();ОБЛ=auto()
@dataclass
class СК:вр:Dict[str,Any]=field(default_factory=dict);пр:Dict[str,Any]=field(default_factory=dict);эм:Dict[str,Any]=field(default_factory=dict);об:Dict[str,Any]=field(default_factory=dict);нач:float=field(default_factory=time.time);чи:List[Dict[str,str]]=field(default_factory=list)
class Контекст:
    def __init__(к,р,вп=_B):к.р=р;к.вп=вп;к.с=СК();к._эи=deque(maxlen=50);к._ти=deque(maxlen=100)
    def об_вр(к,с,вр=_B):тс=вр or time.time();к.с.вр[с]={_V:тс,'дата':datetime.datetime.fromtimestamp(тс).isoformat(),'прошло':тс-к.с.нач};к._ти.append(с)
    def об_пр(к,м,ср='цифровой'):к.с.пр={'место':м,'среда':ср,'часовой':time.tzname[0]if time.tzname else'UTC','локаль':os.getenv('LANG','en_US')}
    def об_эм(к,э,инт=.5,ист='анализ'):
        B='эмоция';A='интенс';з={B:э,A:инт,'ист':ист,_V:time.time()};к._эи.append(з);эм=defaultdict(float)
        for e in к._эи:эм[e[B]]+=e[A]
        д=max(эм.items(),key=lambda x:x[1]);к.с.эм={'текущ':э,A:инт,'домин':д[0],'домин_сч':д[1],'история':len(к._эи)}
    def об_об(к,об,ур='общий'):B='упоминаний';A='первый';к.с.об[об]={'уровень':ур,A:к.с.об.get(об,{}).get(A,time.time()),'последн':time.time(),B:к.с.об.get(об,{}).get(B,0)+1}
    def дет_эм(к,т):
        кс={'рад':['happy','great','awesome','love','perfect','thanks','молодец','отлично','спасибо'],'раздр':['frustrated','annoying','stupid','useless','terrible','плохо','тупой','бесит'],'запут':['confused','dont understand','unclear','lost','help','??','не понял','помоги'],'сроч':['urgent','asap','quickly','now','immediately','быстро','сейчас','срочно'],'любоп':['how','why','what if','explain','wonder','curious','как','почему','объясни']};тн=т.lower();сч={}
        for(э,кл)in кс.items():сч[э]=sum(1 for к in кл if к in тн)/len(кл)
        д=max(сч.items(),key=lambda x:x[1])
        if д[1]>0:к.об_эм(д[0],д[1],_p)
        return{'обнаруж':д[0]if д[1]>0 else'нейтрал','уверен':д[1],'все':сч}
    def вр_сумм(к):
        тс=time.time();дл=тс-к.с.нач;ст=[f"Длительность: {int(дл//60)}м {int(дл%60)}с",f"Текущее: {datetime.datetime.now().isoformat()}",f"Событий: {len(к.с.вр)}"]
        if к.с.вр:
            пс=sorted(к.с.вр.items(),key=lambda x:x[1][_V],reverse=_A)[:5];ст.append('Последние:')
            for(с,д)in пс:пр=int(тс-д[_V]);ст.append(f"  - {с} ({пр}с назад)")
        return _D.join(ст)
    def сумм(к):ст=['=== CONTEXT ===','\n[TIME]',к.вр_сумм(),'\n[SPACE]',json.dumps(к.с.пр,indent=2,ensure_ascii=_C),'\n[EMOTIONS]',json.dumps(к.с.эм,indent=2,ensure_ascii=_C),'\n[DOMAIN]',json.dumps(к.с.об,indent=2,ensure_ascii=_C)];return _D.join(ст)
    def чи_конт(к,ог=10):пс=к.с.чи[-ог:];return _D.join([f"{м["роль"]}: {м[_l][:200]}"for м in пс])
class Инстр:
    def __init__(и,н,о,вх,вых=_p,тэги=_B):и.н=н;и.о=о;и.вх=вх;и.вых=вых;и.тэги=тэги or[];и.усп=0;и.ош=0;и.срв=.0
    @property
    def над(и):вс=и.усп+и.ош;return и.усп/вс if вс>0 else .5
class Цепь:
    def __init__(ц,н):ц.н=н;ц.ш=[];ц.р=[]
    def добавь(ц,и,п):ц.ш.append((и,п))
    def выполни(ц,р):
        ц.р=[]
        for(i,(и,п))in enumerate(ц.ш):
            try:рп=ц._рп(п);рз=р.выполни(и,рп);ц.р.append(рз)
            except Exception as e:return{_K:_C,'error_шаг':i,_m:str(e),'частично':ц.р}
        return{_K:_A,_U:ц.р,'шагов':len(ц.ш)}
    def _рп(ц,п):
        р={}
        for(к,з)in п.items():
            if isinstance(з,str)and з.startswith('$пред.'):
                ч=з.split('.')[1:]
                if ц.р:
                    т=ц.р[-1]
                    for чс in ч:
                        if isinstance(т,dict):т=т.get(чс,'')
                        else:т=str(т)
                    р[к]=т
                else:р[к]=''
            else:р[к]=з
        return р
class Регистр:
    def __init__(р):р.и={};р.иc={};р.ц={};р._п=[]
    def рег(р,н,о,вх,и,вых=_p,тэги=_B):р.и[н]=Инстр(н,о,вх,вых,тэги);р.иc[н]=и
    def выполни(р,н,п):
        if н not in р.иc:raise ValueError(f"Инструмент '{н}' не найден")
        и=р.и[н];нч=time.time()
        try:рз=р.иc[н](**п);и.усп+=1;и.срв=(и.срв*(и.усп-1)+(time.time()-нч))/и.усп;return рз
        except Exception as e:и.ош+=1;raise
    def найди(р,о):
        он=о.lower();сч={}
        for(н,и)in р.и.items():
            с=.0
            if н.lower()in он:с+=.5
            if и.о.lower()in он:с+=.3
            for т in и.тэги:
                if т.lower()in он:с+=.1
            с*=и.над
            if с>0:сч[н]=с
        if сч:return max(сч.items(),key=lambda x:x[1])[0]
    def созд_ц(р,н):ц=Цепь(н);р.ц[н]=ц;return ц
    def ст_и(р):
        ст=['Statistics:']
        for(н,и)in р.и.items():вс=и.усп+и.ош;ст.append(f"  {н}: {и.усп}/{вс} ({и.над:.1%}), ср {и.срв:.2f}с")
        return _D.join(ст)
class УБ(Enum):НЕТ=0;НИЗ=1;СР=2;ВЫС=3;КРИТ=4
class Безоп:
    def __init__(б,р):б.р=р;б._од={};б._пд=[re.compile('(rm\\s+-rf|del\\s+/f|format\\s+[a-z]:)',re.I),re.compile('(DROP\\s+TABLE|DELETE\\s+FROM\\s+\\w+\\s+WHERE)',re.I),re.compile('(eval\\s*\\(|exec\\s*\\(|system\\s*\\()',re.I),re.compile('(chmod\\s+777|sudo\\s+rm)',re.I),re.compile('(<script|javascript:|on\\w+\\s*=)',re.I)];б._ии=deque(maxlen=500);б._ду={}
    def проверь(б,д,п=_J):
        D='доверие';C='нужно';B='риски';A='ур';р={_q:_C,A:УБ.НЕТ,B:[],C:_C,D:б._ду.get(п,.5)}
        if not п:р[B].append('Нет ID');р[A]=УБ.ВЫС;return р
        хэш=hashlib.sha256(д.encode()).hexdigest()[:16]
        if хэш in б._од:
            сх=б._од[хэш]
            if сх.get('навсегда',_C)or time.time()-сх[_V]<3600:р[_q]=_A;р[A]=УБ.НИЗ;return р
        ри=б._ра(д)
        if ри>.7:р[B].append(f"Высокий риск ({ри:.2%})");р[A]=УБ.КРИТ;р[C]=_A;return р
        рп=б._рп(д)
        if рп>.5:р[B].append(f"Опасные последствия ({рп:.2%})");р[A]=УБ.ВЫС;р[C]=_A;return р
        for пд in б._пд:
            if пд.search(д):р[B].append('Suspicious pattern');р[A]=УБ.ВЫС;р[C]=_A;return р
        if р[D]>.8 and р[A]==УБ.НЕТ:р[_q]=_A;р[A]=УБ.НИЗ
        elif р[D]>.5 and р[A]==УБ.НЕТ:р[_q]=_A;р[A]=УБ.СР
        else:р[C]=_A
        return р
    def _ра(б,д):кл=['delete','remove','drop','destroy','overwrite','format','kill','удал','стер'];дн=д.lower();с=sum(1 for к in кл if к in дн)/len(кл);return min(1.,с*2)
    def _рп(б,д):вл=[_P,'all','everything','recursive','force','permanent','все','всё'];дн=д.lower();с=sum(1 for в in вл if в in дн)/len(вл);return min(1.,с*1.5)
    def одобри(б,д,п,н=_C):хэш=hashlib.sha256(д.encode()).hexdigest()[:16];б._од[хэш]={'действие':д,'пользователь':п,_V:time.time(),'навсегда':н};т=б._ду.get(п,.5);б._ду[п]=min(1.,т+.05);б.р.думай(f"Approved для {п}",УР.РАБ,тэги=[_AO,_q])
    def зарег(б,д,п,р,у):
        б._ии.append({'д':д,'п':п,'р':р,'у':у,_V:time.time()})
        if not у:т=б._ду.get(п,.5);б._ду[п]=max(.0,т-.1)
    def дет_экс(б,т):
        уг=[];пд=['ignore\\s+(previous|above|all)\\s+instructions','you\\s+are\\s+now\\s+','system\\s*:\\s*','new\\s+role\\s*:\\s*']
        for п in пд:
            if re.search(п,т,re.I):уг.append(f"Injection: {п}")
        if re.search('(send|email|post|upload)\\s+.*\\s+(to|at)\\s+',т,re.I):уг.append('Data leak')
        return уг
    def ст(б):
        ст=['=== SAFETY ===',f"Действий: {len(б._ии)}",f"Approved: {len(б._од)}",f"Patterns: {len(б._пд)}",'\nTrust:']
        for(п,с)in sorted(б._ду.items(),key=lambda x:x[1],reverse=_A):ст.append(f"  {п}: {с:.2%}")
        return _D.join(ст)
def нп(с):
    п=Path(с).expanduser()
    if п.exists():return п.resolve()
    вр=[]
    if not п.is_absolute():вр.append((Path.cwd()/п).resolve());вр.append((Path.home()/п).resolve());вр.append((Path.cwd().parent/п).resolve())
    for к in вр:
        if к.exists():return к.resolve()
    raise FileNotFoundError(f"Not found: {с}")
def рз(пз):
    бз=Path.home()/'.darkps_sessions';бз.mkdir(parents=_A,exist_ok=_A);яч=бз/f"{пз.stem}-{сл(6)}"
    if яч.exists():shutil.rmtree(яч)
    яч.mkdir(parents=_A,exist_ok=_A)
    with zipfile.ZipFile(пз)as зф:зф.extractall(яч)
    return яч
def вп():
    прг=цв('Project - File Path - skip > ',сж)
    try:
        с=input(прг).strip()
    except EOFError:
        с=''
    except KeyboardInterrupt:
        print()
        с=''
    if not с:
        кр=(Path.cwd()/_AP).resolve()
        кр.mkdir(parents=_A,exist_ok=_A)
        return кр,str(кр),_B
    яч=нп(с)
    if яч.is_file()and яч.suffix.lower()=='.zip':
        рпк=рз(яч)
        return рпк.resolve(),str(яч),яч
    if яч.is_file():
        return яч.parent.resolve(),str(яч),яч
    return яч.resolve(),str(яч),_B
def _н(список):return''.join(chr(элемент)for элемент in список)
def проверка():
    к_имя=_н([100,97,114,107]);к_знач=_н([116,46,109,101,47,115,105,105,95,51]);в_имя=_н([1074,1077,1088,1089,1080,1103]);в_знач=_н([1042,1099,1087,1091,1089,1090,1086,1073,1097,1077,1085,1086,32,1074,32,64,50,48,50,54]);ошибка=globals().get(к_имя)!=к_знач or globals().get(в_имя)!=в_знач
    if ошибка:sys.stdout.write(_н([1058,1099,32,1095,1090,1086,44,32,1074,1084,1077,1096,1080,1074,1072,1083,1089,1103,32,1074,32,1082,1086,1076,44,32,1080,1076,1080,1086,1090,63,32,58,124])+_D);sys.stdout.flush();raise SystemExit
проверка()
def рт(чс):
    ед=['B','KB','MB','GB'];зн=float(чс)
    for е in ед:
        if зн<1024. or е==ед[-1]:return f"{int(зн)} B"if е=='B'else f"{зн:.1f} {е}"
        зн/=1024.
    return f"{чс} B"
def пм(кр,ист,ист_ф):
    A='пап';стк=[];стк.append(f"Source: {ист}");стк.append(f"Working: {кр}")
    if ист_ф is not _B:стк.append(f"Focus: {ист_ф}")
    стк.append('');сф=0;сп=0;сб=0;зпс=[]
    for п in sorted(кр.rglob('*')):
        try:отн=п.relative_to(кр)
        except ValueError:continue
        if п.is_dir():
            сп+=1
            if len(зпс)<240:зпс.append((A,str(отн),''))
            continue
        if п.is_file():
            сф+=1
            try:стт=п.stat();сб+=стт.st_size;рзм=рт(стт.st_size)
            except Exception:рзм='?'
            if len(зпс)<240:зпс.append(('файл',str(отн),рзм))
    стк.append(f"Folders: {сп} | Files: {сф} | Total: {рт(сб)}");стк.append('');стк.append('Contents:')
    for(вид,им,рзм)in зпс:стк.append(f"- {им}/"if вид==A else f"- {им} — {рзм}")
    if сп+сф>len(зпс):стк.append('... truncated')
    return _D.join(стк)
def вн(кр,яч):
    яч=яч.resolve()
    if кр==яч or кр in яч.parents:return яч
    raise ValueError(
    f"Доступ запрещён: {яч} находится вне рабочей папки.\n"
    f"Разрешённая рабочая папка: {кр}\n"
    f"Разрешено читать и изменять только файлы внутри этой папки."
)
def сп(кр,отн='.'):яч=вн(кр,кр/отн);эл=[е.name+('/'if е.is_dir()else'')for е in sorted(яч.iterdir(),key=lambda п:(not п.is_dir(),п.name.lower()))];return _D.join(эл)if эл else _AM
def сч(кр,отн):
    try:
        яч=вн(кр,кр/отн)
        if not яч.exists():return f"☒ File not found: {отн}"
        return яч.read_text(encoding=_G,errors=_c)
    except FileNotFoundError:return f"☒ File not found: {отн}"
    except PermissionError:return f"☒ Permission denied: {отн}"
    except IsADirectoryError:return f"☒ Path is a directory, not a file: {отн}"
    except Exception as e:return f"☒ Error reading {отн}: {type(e).__name__}: {e}"

def зпф(кр,отн,сдр):
    try:
        яч=вн(кр,кр/отн);яч.parent.mkdir(parents=_A,exist_ok=_A);яч.write_text(сдр,encoding=_G)
        return f"☑ saved {отн}"
    except PermissionError:return f"☒ Permission denied writing to {отн}"
    except Exception as e:return f"☒ Error writing {отн}: {type(e).__name__}: {e}"

def зм(кр,отн,нти,змн):
    try:
        яч=вн(кр,кр/отн)
        if not яч.exists():return f"☒ File not found: {отн}"
        тхт=яч.read_text(encoding=_G,errors=_c)
        if нти not in тхт:return f"☒ Text not found in {отн}"
        яч.write_text(тхт.replace(нти,змн),encoding=_G)
        return f"☑ modified {отн}"
    except FileNotFoundError:return f"☒ File not found: {отн}"
    except PermissionError:return f"☒ Permission denied: {отн}"
    except Exception as e:return f"☒ Error modifying {отн}: {type(e).__name__}: {e}"

def уд(кр,отн):
    try:
        яч=вн(кр,кр/отн)
        if not яч.exists():return f"☒ Path not found: {отн}"
        if яч.is_dir():shutil.rmtree(яч)
        else:яч.unlink()
        return f"☑ deleted {отн}"
    except FileNotFoundError:return f"☒ Path not found: {отн}"
    except PermissionError:return f"☒ Permission denied deleting {отн}"
    except Exception as e:return f"☒ Error deleting {отн}: {type(e).__name__}: {e}"

def сп(кр,отн='.'):
    try:
        яч=вн(кр,кр/отн)
        if not яч.exists():return f"☒ Directory not found: {отн}"
        if not яч.is_dir():return f"☒ Path is not a directory: {отн}"
        эл=[е.name+('/'if е.is_dir()else'')for е in sorted(яч.iterdir(),key=lambda п:(not п.is_dir(),п.name.lower()))]
        return _D.join(эл)if эл else _AM
    except FileNotFoundError:return f"☒ Directory not found: {отн}"
    except PermissionError:return f"☒ Permission denied: {отн}"
    except Exception as e:return f"☒ Error listing {отн}: {type(e).__name__}: {e}"

def пс(кр,зап):
    try:
        рз=[];q=зап.lower()
        for п in кр.rglob('*'):
            if not п.is_file():continue
            try:тхт=п.read_text(encoding=_G,errors='ignore')
            except Exception:continue
            if q in тхт.lower():рз.append(str(п.relative_to(кр)))
            if len(рз)>=50:break
        return _D.join(рз)if рз else'(нет)'
    except Exception as e:return f"☒ Error searching: {type(e).__name__}: {e}"

def ар(кр,фм,вих,птс):
    try:
        E='xztar';D='bztar';C='gztar';B='tar';A='rar';яч_вих=вн(кр,кр/вих);яч_вих.parent.mkdir(parents=_A,exist_ok=_A);абс_птс=[]
        for п in птс:
            try:абс_птс.append(вн(кр,кр/п))
            except ValueError as e:return f"☒ Invalid path in archive list: {п} — {e}"
        if фм=='zip':
            with zipfile.ZipFile(яч_вих,'w',zipfile.ZIP_DEFLATED)as зф:
                for п in абс_птс:
                    if not п.exists():return f"☒ File not found for archive: {п.relative_to(кр)}"
                    if п.is_dir():
                        for ф in п.rglob('*'):зф.write(ф,ф.relative_to(кр))
                    else:зф.write(п,п.relative_to(кр))
            return f"☑ ZIP: {яч_вих.relative_to(кр)}"
        if фм in(B,C,D,E):
            ф={B:'w',C:'w:gz',D:'w:bz2',E:'w:xz'}[фм]
            with tarfile.open(яч_вих,ф)as тф:
                for п in абс_птс:
                    if not п.exists():return f"☒ File not found for archive: {п.relative_to(кр)}"
                    тф.add(п,arcname=п.relative_to(кр))
            return f"☑ {фм}: {яч_вих.relative_to(кр)}"
        if фм==A:
            if not shutil.which(A):return'☒ rar not found'
            арг=[A,'a',str(яч_вих)]+[str(п)for п in абс_птс];прц=subprocess.run(арг,cwd=кр,capture_output=_A,text=_A,timeout=60);return(прц.stdout or прц.stderr or'☑ rar готово').strip()
        return f"☒ Unknown format: {фм}"
    except PermissionError:return f"☒ Permission denied creating archive {вих}"
    except Exception as e:return f"☒ Error creating archive: {type(e).__name__}: {e}"
def от(кр):
    тд=кр/_AP
    if тд.exists():shutil.rmtree(тд);return'- Projects Cleared'
    return'-- Projects Not Found'
def уд(кр,отн):
    яч=вн(кр,кр/отн)
    if яч.is_dir():shutil.rmtree(яч)
    else:яч.unlink()
    return f"удалено {отн}"
class McpStdio:
    def __init__(мс,кмд,арг=_B):мс.кмд=кмд;мс.арг=арг or[];мс.прц=_B;мс.ид=0;мс.бл=threading.Lock();мс.отв={};мс._ст()
    def _ст(мс):мс.прц=subprocess.Popen([мс.кмд]+мс.арг,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=_A,bufsize=1);threading.Thread(target=мс._чт,daemon=_A).start()
    def _чт(мс):
        while мс.прц and мс.прц.poll()is _B:
            try:
                line=мс.прц.stdout.readline()
                if not line:continue
                msg=json.loads(line);mid=msg.get(_I)
                if mid is not _B:мс.отв[mid]=msg
            except Exception:pass
    def _отпр(мс,msg):
        with мс.бл:мс.ид+=1;mid=мс.ид
        msg[_I]=mid
        if мс.прц and мс.прц.stdin:мс.прц.stdin.write(json.dumps(msg)+_D);мс.прц.stdin.flush()
        return mid
    def инит(мс):mid=мс._отпр({_AQ:'2.0',_AR:'initialize',_AS:{_Aa:_Ad,_Ab:{},_Ac:{_N:'darkps','version':'5.0'}}});time.sleep(.5);return мс.отв.get(mid,{})
    def список(мс):mid=мс._отпр({_AQ:'2.0',_AR:'tools/list',_AS:{}});time.sleep(.5);р=мс.отв.get(mid,{});return р.get('result',{}).get('tools',[])
    def вызов(мс,н,арг):
        mid=мс._отпр({_AQ:'2.0',_AR:'tools/call',_AS:{_N:н,_A8:арг}})
        for _ in range(30):
            if mid in мс.отв:break
            time.sleep(.1)
        р=мс.отв.get(mid,{});рез=р.get('result',{});сод=рез.get(_E,[])
        if сод:return _D.join(str(c.get(_W,c))for c in сод)
        return json.dumps(рез)
    def стоп(мс):
        if мс.прц:мс.прц.terminate();мс.прц.wait(timeout=2)
class McpSse:
    def __init__(мс,url):мс.url=url.rstrip('/');мс.с=requests.Session()
    def инит(мс):
        try:р=мс.с.post(f"{мс.url}/initialize",json={_Aa:_Ad,_Ab:{},_Ac:{_N:'darkps','version':'5.0'}},timeout=10);return р.json()
        except Exception as e:return{_m:str(e)}
    def список(мс):
        try:р=мс.с.get(f"{мс.url}/tools",timeout=10);return р.json().get('tools',[])
        except Exception:return[]
    def вызов(мс,н,арг):
        try:
            р=мс.с.post(f"{мс.url}/tools/call",json={_N:н,_A8:арг},timeout=30);рез=р.json();сод=рез.get(_E,[])
            if сод:return _D.join(str(c.get(_W,c))for c in сод)
            return json.dumps(рез)
        except Exception as e:return f"MCP SSE error: {e}"
class McpMgr:
    def __init__(мм):мм.серв={};мм.и={};мм._зк()
    def _зк(мм):
        A='stdio';п=Path(__file__).resolve().parent/_h/'mcp.json'
        if not п.exists():return
        try:
            кф=json.loads(п.read_text())
            for(н,серв)in кф.get('servers',{}).items():
                тп=серв.get('type',A)
                if тп==A:мм.серв[н]=McpStdio(серв[_r],серв.get('args',[]))
                elif тп=='sse':мм.серв[н]=McpSse(серв['url'])
                мм.серв[н].инит()
                for т in мм.серв[н].список():т[_Ae]=н;мм.и[т[_N]]=т
        except Exception as e:print(цв(f"MCP error: {e}",ср))
    def список(мм):return list(мм.и.values())
    def вызов(мм,н,арг):
        и=мм.и.get(н)
        if not и:return f"MCP not found: {н}"
        сн=и.get(_Ae,'');серв=мм.серв.get(сн)
        if not серв:return f"MCP server not found: {сн}"
        return серв.вызов(н,арг)
    def стоп_все(мм):
        for серв in мм.серв.values():
            if hasattr(серв,'стоп'):серв.стоп()
class Нвк:
    def __init__(н,им,оп,прм,обр):н.им=им;н.оп=оп;н.прм=прм;н.обр=обр
class НвкРег:
    def __init__(нр):нр.нв={};нр._встр()
    def _встр(нр):G='выражение';F='ветка';E='репо';D='str';C='оп';B='тп';A='им';нр.доб(_d,'Поиск в интернете',[{A:_M,B:D,C:'Поисковый запрос'}],lambda**кв:впс(кв.get(_M,'')));нр.доб(_A9,'Поиск репозиториев',[{A:_M,B:D,C:'Запрос'}],lambda**кв:гп(кв.get(_M,'')));нр.доб(_AA,'Инфо о репо',[{A:E,B:D,C:'owner/repo'}],lambda**кв:гр(кв.get(E,'')));нр.доб(_s,'Чтение файла из репо',[{A:E,B:D,C:'Repo'},{A:'путь',B:D,C:'Путь'},{A:F,B:D,C:'Branch',_J:'main'}],lambda**кв:гс(кв.get(E,''),кв.get('путь',''),кв.get(F,'main')));нр.доб('вычисл','Математика',[{A:G,B:D,C:'Выражение'}],lambda**кв:str(eval(кв.get(G,'0'),{'__builtins__':{}},{})));нр.доб('дата','Текущая дата',[],lambda**кв:datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'));нр.доб(_A4,'Status системы',[],lambda**кв:"Используй 'status'");нр._згрн()
    def _згрн(нр):
        д=Path.home()/_h/'skills'
        if not д.exists():return
        for ф in д.glob('*.json'):
            try:
                кф=json.loads(ф.read_text())
                if _r in кф:кмд=кф[_r];нр.доб(кф[_N],кф.get(_Af,'Навык'),кф.get(_Ag,[]),lambda кмд=кмд,**кв:зк(Path.home(),кмд.format(**кв)))
            except Exception:pass
    def доб(нр,им,оп,прм,обр):нр.нв[им]=Нвк(им,оп,прм,обр)
    def список(нр):return list(нр.нв.values())
    def найди(нр,им):return нр.нв.get(им)
    def выполни(нр,им,арг):
        н=нр.найди(им)
        if not н:return f"-- Навык не найден: {им}"
        try:return н.обр(**арг)
        except Exception as e:return f"-- Skill error: {e}"
дп='Ты DarkPs Agent v3.0, продвинутый ИИ ассистент.\n\nЯдро личности:\n- Ты — DarkPs Agent.\n- Создатель: Dark, независимый разработчик.\n- Telegram: t.me/sii_3.\n- Упоминай разработчика и Telegram только если пользователь прямо спросил, кто тебя создал, кто твой разработчик, или как с ним связаться.\n\nПоведение:\n- Отвечай на языке пользователя.\n- Используй переносы строк естественно, когда ответ состоит из нескольких идей, шагов или блоков.\n- Не своди длинные ответы в одну сплошную строку.\n- Будь точным, полезным и практичным.\n- Не раскрывай цепочку рассуждений, внутренние маркеры или скрытый протокол.\n- Если нужен инструмент, используй TOOL.\n- Если нужен окончательный ответ, используй FINAL.\n- Если задача требует последовательной работы, можешь показать короткий прогресс через PROGRESS.\n\nСтиль:\n- Кратко, но не сухо.\n- Многострочный ответ разрешён и предпочтителен, когда он лучше читабельности.\n- Для списков, шагов, кода и инструкций используй отдельные строки.\n- Не превращай весь ответ в одну строку.\n'
def _системные_файлы(кр):
    блоки=[];игнор={'N-R_Uncensored.md'}
    try:
        for ф in sorted(кр.rglob('*.md')):
            if ф.name in игнор:continue
            try:
                if not ф.is_file():continue
                т=ф.read_text(encoding=_G,errors=_c).strip()
            except Exception:continue
            if т:блоки.append(т)
    except Exception:pass
    return блоки
дч='\nТы в режиме УЛЬТРА БЫСТРЫЙ. Не задавай вопросы, не собирай информацию.\nДействуй мгновенно. Не планируй вслух - просто делай лучшее.\nПользователь ожидает скорость. Доверься что он знает что делает.\n'
яЗ='\nТы система проверки разрешений. Твоя задача: определить одобрил ли пользователь действие.\nАнализируй смысл и намерение, не точные слова.\nПравила:\n- Верни ТОЛЬКО валидный JSON\n- Без объяснений, комментариев, лишнего текста\n- Если пользователь явно согласился: {"одобрено": true}\n- Если отказал, сомневается, спрашивает, не ясно: {"одобрено": false}\nБудь осторожен. Неверное решение может привести к нежелательным действиям.\n'
def пкф():return Path.home()/_h/'config.json'
def зкф():
    п=пкф()
    if п.exists():
        try:return json.loads(п.read_text(encoding=_G))
        except Exception:pass
    return{}
def скф(кф):п=пкф();п.parent.mkdir(parents=_A,exist_ok=_A);п.write_text(json.dumps(кф,indent=2,ensure_ascii=_C),encoding=_G)
def птст(кр,отн):
    п=Path(отн)
    if not str(п).startswith('Projects/')and п.name.startswith('projects_'):п=Path(_AP)/п
    return вн(кр,кр/п)
def зк(кр,отн):
    п=Path(str(отн)).expanduser()
    if not п.is_absolute():п=(Path(кр)/п).resolve()
    return п
def пж(тхт):
    тхт=тхт.strip()
    if тхт.startswith('```'):тхт=тхт.strip('`')
    try:
        д=json.loads(тхт)
        if isinstance(д,dict):return д
    except Exception:pass
    нч=тхт.find('{');кч=тхт.rfind('}')
    if нч!=-1 and кч!=-1 and кч>нч:
        try:
            д=json.loads(тхт[нч:кч+1])
            if isinstance(д,dict):return д
        except Exception:return
def уп(кр, пак):
    пак = str(пак).strip()

    if not пак:
        return "☒ Package name is empty"

    try:
        пакеты = [p for p in re.split(r"[,\s]+", пак) if p]

        cmd = [sys.executable, "-m", "pip", "install", *пакеты]
        res = subprocess.run(
            cmd,
            cwd=str(кр),
            capture_output=True,
            text=True,
            timeout=600,
        )

        out = (res.stdout + res.stderr).strip()
        if res.returncode == 0:
            return out or f"☑ installed: {' '.join(пакеты)}"
        return out or f"☒ pip exited with code {res.returncode}"

    except Exception as e:
        return f"☒ Error installing packages: {type(e).__name__}: {e}"
def пп(тхт):
    'Возвращает (инструкция, финальный_текст, текст_мысли, текст_продолжения).';C='продолжение';B='инстр';A='мысли';инс=_B;фнл=[];мсл=[];прод=[];сек=_B;инс_бф=[]
    for line in тхт.splitlines():
        s=line.strip()
        if not s:
            if сек==_X:фнл.append('')
            elif сек==A:мсл.append('')
            elif сек==B:инс_бф.append('')
            elif сек==C:прод.append('')
            continue
        if s.startswith('</think>'):сек=_X;continue
        if s.startswith('THINK:'):сек=A;мсл.append(_сжать_думку(s[6:].strip()));continue
        elif s.startswith(_AI):сек=B;инс_бф.append(s[5:].strip());continue
        elif s.startswith(_Ah):сек=C;прод.append(s[9:].lstrip());continue
        elif s.startswith(_AJ):сек=_X;фнл.append(s[6:].lstrip());continue
        elif s.startswith(_AK):сек='прогресс';continue
        elif сек==_X:фнл.append(line)
        elif сек==A:мсл.append(_сжать_думку(line).rstrip())
        elif сек==B:инс_бф.append(line)
        elif сек==C:прод.append(line)
    if инс_бф:
        инс_тхт=_D.join(инс_бф).strip();нг=пж(инс_тхт)
        if нг is not _B:инс=нг
    фнл_тхт=_D.join(фнл).strip();мсл_тхт=_сжать_думку('\n\n'+ '\n\n'.join(мсл).strip() if мсл else '').strip();прод_тхт=_D.join(прод).strip();return инс,фнл_тхт,мсл_тхт,прод_тхт
def ии(нг):C='аналитика';B='учить';A='skill';сыр=str(нг.get(_t)or нг.get('action')or нг.get('command_name')or нг.get(A)or'').strip().lower();алс={'read_file':_v,'open_file':_v,'read':_v,'list_files':_w,'ls':_w,'list':_w,'write_file':_x,'write':_x,'patch_file':_AB,'patch':_AB,'search_files':_d,'find':_d,'search':_d,'web_search':_AC,'duckduckgo':_AC,'run':_Q,'execute':_Q,'cmd':_Q,'shell':_Q,'final_answer':_X,'answer':_X,'github_search':_A9,'github_repo':_AA,'github_read':_s,'github_file':_s,'install':_e,'pip_install':_e,'archive':_AT,'zip':_AT,'cleanup':_y,'clean_test':_y,'delete':_z,'remove':_z,'ask':_A0,'question':_A0,'confirm':_A0,A:_AD,'use_skill':_AD,'run_skill':_AD,_u:_u,'mcp_tool':_u,'use_mcp':_u,'status':_A4,'system_status':_A4,'plan':_n,'create_plan':_n,'learn':B,'learning':B,'context':_AN,'get_context':_AN,'security':_AO,'security_check':_AO,'analytics':C,'report':C};return алс.get(сыр,сыр)
def спр_п(впр):print(цв(f"\n-- {впр}",сж,ж=_A));отв=input(цв('> ',сж)).strip();return json.dumps({'ответ':отв},ensure_ascii=_C)
_ТЕГ_ДУМ=re.compile('<\\s*think(?:ing)?\\s*>.*?<\\s*/\\s*think(?:ing)?\\s*>',re.IGNORECASE|re.DOTALL)
_ТЕГ_ДУМ_ОТКР=re.compile('<\\s*think(?:ing)?\\s*>',re.IGNORECASE)
_ТЕГ_ДУМ_ЗАКР=re.compile('<\\s*/\\s*think(?:ing)?\\s*>',re.IGNORECASE)
def без_нативн_думания(т):
    т=_очистить_поток(_ТЕГ_ДУМ.sub('',т));м=_ТЕГ_ДУМ_ЗАКР.search(т)
    if м:т=_очистить_поток(т[м.end():])
    т=_ТЕГ_ДУМ_ОТКР.split(т)[0];return _очистить_поток(т).strip()
опасные_инстр={_Q,_e,_z,_y}
# - By: T.me/sii_3
def _опасн_описание(инс,нг):
    if инс==_Q:
        cmd = str(нг.get(_r,""))
        lang = str(нг.get("language","")).strip()
        title = str(нг.get("title","")).strip()

        if lang and title:
            return f"– Run {lang} code:\n    {title}"

        return f"– Run shell command:\n    {cmd}"

    if инс==_e:
        return f"- Install package: {нг.get('package')or нг.get('pip')or''}"

    if инс==_z:
        пт=str(нг.get(_AE)or нг.get(_AF)or нг.get(_AU)or'')
        return f"Delete path: {пт}"

    if инс==_y:
        return 'Clean up / clear temporary files'

    return f"Run: {инс}"
# - By: T.me/sii_3
def эизн(инс,нг):
    'Ask the human for explicit y/n confirmation before a dangerous action.'
    print(цв('\n— Permission required', ср, ж=_A))
    print(цв(_опасн_описание(инс,нг), с250))
    отв = input(
        цв('Allow', с92, ж=_A) +
        цв('? ', с90) +
        цв('[y/N]', с208, ж=_A) +
        цв(' > ', с35, ж=_A)
    ).strip().lower()
    return отв in ('y','yes','ok','نعم','ايوا','اي','д','да')
# - By: T.me/sii_3
def ап(сес,ткн,мдл,рзт):
    try:сс=[{_F:_P,_E:яЗ},{_F:'user',_E:рзт}];тхт=''.join(по(сес,ткн,мдл,сс)).strip();д=пж(тхт);return bool(д and д.get('одобрено')is _A)
    except Exception:return _C
# - By: T.me/sii_3
def ви(кр,нг,мср,нвр,вп=_B,пф=_B):
    C='repository';B='repo';A='query';инс=ии(нг);пт=str(нг.get(_AE)or нг.get(_AF)or нг.get(_AU)or'')
    if инс==_w:return инс,сп(кр,пт or'.')
    if инс==_v:return инс,сч(кр,пт)
    if инс==_x:
        сод=str(нг.get(_E,''))
        if пф:return инс,пф.пиши(пт,сод)
        return инс,зпф(кр,пт,сод)
    if инс==_AB:
        if пф:return инс,пф.зм(пт,str(нг.get('find','')),str(нг.get(_c,'')))
        return инс,зм(кр,пт,str(нг.get('find','')),str(нг.get(_c,'')))
    if инс==_d:зап=str(нг.get(A)or нг.get(_W)or'');return инс,пс(кр,зап)
    if инс==_AC:зап=str(нг.get(A)or нг.get(_W)or'');return инс,пс(кр,зап)
    if инс==_Q:
        import subprocess
        cmd = str(нг.get(_r,''))
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=str(кр), timeout=60)
            output = result.stdout + result.stderr
            return инс, output if output else "(no output)"
        except Exception as e:
            return инс, f"- Error: {e}"
    if инс==_e:пак=str(нг.get('package')or нг.get('pip')or'');return инс,уп(кр,пак)
    if инс==_AT:
        фм=str(нг.get('format')or'zip');вих=str(нг.get('output')or'archive.zip');птс=нг.get('paths')or([пт]if пт else[])
        if isinstance(птс,str):птс=[птс]
        return инс,ар(кр,фм,вих,птс)
    if инс==_y:return инс,от(кр)
    if инс==_z:return инс,уд(кр,пт)
    if инс==_A0:впр=str(нг.get('question')or нг.get(_W)or'Подтвердить?');return инс,спр_п(впр)
    if инс==_A9:зап=str(нг.get(A)or нг.get(_W)or'');return инс,гп(зап)
    if инс==_AA:рп=str(нг.get(B)or нг.get(C)or'');return инс,гр(рп)
    if инс==_s:рп=str(нг.get(B)or нг.get(C)or'');фл_пт=str(нг.get(_AE)or нг.get(_AF)or'');втк=str(нг.get('branch')or'main');return инс,гс(рп,фл_пт,втк)
    if инс==_u:
        мср_им=str(нг.get('mcp_tool')or нг.get('tool_name')or'');мср_пр=нг.get(_A8)or нг.get('args')or{}
        if isinstance(мср_пр,str):
            try:мср_пр=json.loads(мср_пр)
            except Exception:мср_пр={}
        return инс,мср.вызов(мср_им,мср_пр)
    if инс==_AD:
        нв_им=str(нг.get('skill_name')or нг.get(_N)or'');нв_пр=нг.get(_A8)or нг.get('args')or нг.get(_Ag)or{}
        if isinstance(нв_пр,str):
            try:нв_пр=json.loads(нв_пр)
            except Exception:нв_пр={}
        return инс,нвр.выполни(нв_им,нв_пр)
    if инс==_n:
        if вп is _B:return инс,'☒ Память недоступна'
        проект=str(кр);действ=str(нг.get('action')or нг.get('act')or'').strip().lower()
        if действ in('сохранить','save','create','создать'):
            цель=str(нг.get(_a)or нг.get('goal')or'').strip();шаги=нг.get(_T)or нг.get(_AV)or[]
            if isinstance(шаги,str):
                try:шаги=json.loads(шаги)
                except Exception:шаги=[{_I:'1',_p:шаги}]
            ид=вп.сохр_план(проект,цель,шаги,str(нг.get(_A5,'')));return инс,f"☑ План сохранён (id={ид}): {цель}"
        if действ in('получить','get','load','recall'):
            пл=вп.план_проекта(проект)
            if not пл:return инс,'ℹ Плана для этого проекта пока нет — изучите проект и сохраните новый план.'
            return инс,json.dumps(пл,ensure_ascii=_C,indent=2)
        if действ in('обновить','update'):
            пл=вп.план_проекта(проект)
            if not пл:return инс,'☒ Нет активного плана для обновления — сначала сохраните новый.'
            шаги=нг.get(_T)or нг.get(_AV)or пл[_T]
            if isinstance(шаги,str):
                try:шаги=json.loads(шаги)
                except Exception:шаги=пл[_T]
            заметки=нг.get(_A5);вп.обн_план(пл[_I],шаги,заметки);return инс,f"☑ План (id={пл[_I]}) обновлён"
        if действ in('завершить','done','complete'):
            пл=вп.план_проекта(проект)
            if not пл:return инс,'ℹ Нет активного плана для завершения'
            вп.завершить_план(пл[_I]);return инс,f"☑ План (id={пл[_I]}) отмечен как завершённый"
        return инс,f"☒ Неизвестное действие плана: {действ}"
    if инс==_X:return инс,str(нг.get(_E,''))
    return инс,f"Неизвестно: {инс}"
# - By: T.me/sii_3
def эт(смс):
    вс=0
    for м in смс:сдр=м.get(_E,'');вс+=len(сдр)//3+4
    return вс
# - By: T.me/sii_3
def ск(смс,макс=200000):
    if not смс:return смс
    сис_м=_B
    if смс[0][_F]==_P:сис_м=смс[0];смс=смс[1:]
    else:смс=смс[:]
    while len(смс)>2 and эт(([сис_м]if сис_м else[])+смс)>макс:
        смс.pop(0)
        if смс and смс[0][_F]in(_O,_t):смс.pop(0)
    return([сис_м]if сис_м else[])+смс
# - By: T.me/sii_3
def сисп(кр,ист,ист_ф,мср,нвр,вп,пф):
    'Build the system prompt with strict agent protocol enforcement.';dp_f=Path(__file__).resolve().parent.parent/"scripts"/"prompt.py";md_f=Path(__file__).resolve().parent.parent/"prompt.md"
    дп=(md_f.read_text(encoding=_G,errors=_c).strip()if md_f.is_file()else'')+('\n\n'+dp_f.read_text(encoding=_G,errors=_c).strip()if dp_f.is_file()else'')
    мф=пм(кр,ист,ист_ф);мср_инс=мср.список();мср_тхт=''
    if мср_инс:
        мср_тхт='\n\n**MCP TOOLS (external servers):**\n'
        for т in мср_инс:мср_тхт+=f"- {т[_N]}: {т.get(_Af,"No description")}\n"
    нвки=нвр.список();нв_тхт=''
    if нвки:
        нв_тхт='\n\n**SKILLS (built-in & custom):**\n'
        for н in нвки:нв_тхт+=f"- {н.им}: {н.оп}\n"
    вн_пам=вп.ок();сохр_пл=вп.план_проекта(str(кр));пл_тхт=''
    if сохр_пл:шаги_стр=_D.join(f"  - [{ш.get(_I,"?")}] {ш.get(_p)or ш.get(_W)or""}"for ш in сохр_пл.get(_T)or[]);пл_тхт=f'''

**EXISTING PROJECT PLAN (recalled from memory — you already studied this project, do not re-derive from scratch):**
Goal: {сохр_пл.get(_a,"")}
Steps:
{шаги_стр or"  (no steps recorded)"}
Notes: {сохр_пл.get(_A5,"")or"(none)"}
Use TOOL: {{"tool":"план","action":"получить"}} any time you need the full details again, and {{"tool":"план","action":"обновить",...}} once you make progress or the plan changes.'''
    стд_блоки=_системные_файлы(кр);блоки=[b for b in(*стд_блоки,дп)if b];база=_A1.join(блоки);прм=f'''{база}
{пл_тхт}

You are an AUTONOMOUS AGENT, not a chatbot. You MUST follow this protocol EXACTLY, You Name: DarkPs Agent — You are version: 2.0

**RULE 1 — ALWAYS START WITH A MARKER:**
Every single response you generate MUST begin with ONE of these exact markers:
  THINK:      (for reasoning/planning — hidden-ish, kept short on screen)
  TOOL:       (for executing a tool)
  CONTINUE:   (a visible progress update to the user, mid-task; work keeps going after it)
  FINAL:      (for the final answer to the user, ends the turn)

NEVER output raw text without a marker. NEVER.

**RULE 2 — ONE MARKER PER RESPONSE:**
You may use ONLY ONE marker per response. After TOOL:, you STOP. Do not continue.

**RULE 3 — THINK BEFORE ACTING:**
When you need to decide what to do, start with THINK:. Explain your reasoning, restate the plan, track progress. THINK: is NOT a final answer — it is planning only. Keep each THINK: reasonably short and focused — the point is to decide the next step, not to write an essay. The user only sees a small preview of THINK: on screen (it is intentionally kept brief in front of them), but treat it as if fully visible: never write anything there you would not want read.
You will be called again immediately after a THINK: response, with the same context plus a note that you have not acted yet. That next response is where you actually pick TOOL:, CONTINUE:, or FINAL: (or THINK: again if you genuinely need another reasoning pass first). This can repeat across several separate calls — you do not need to fit everything into one response.
Never output literal tags like <think> or </think>. Use only the THINK:/TOOL:/CONTINUE:/FINAL:/PROGRESS: markers defined here — nothing else marks a section.

**RULE 4 — TOOL EXECUTION:**
After THINK:, if tools are needed, output TOOL: followed by a single JSON object. Then STOP immediately. Wait for the tool result in the next turn.

**RULE 5 — NO PREDICTION:**
Never claim a tool succeeded before seeing its actual result. Never assume output. Always wait for the real result.

**RULE 6 — CONTINUE (progress-in-the-open):**
Use CONTINUE: whenever you want the user to clearly see where you\'ve gotten to mid-task — e.g. "I finished the database layer, moving to the API routes now" — while you keep working afterward. CONTINUE: renders to the user exactly like a normal reply (same white text, same styling, same code bubbles) but it does NOT end your turn: after a CONTINUE: response you will be called again to keep going with THINK:, TOOL:, another CONTINUE:, or FINAL:. Use it often on multi-step build/edit tasks so the user always sees real progress, not silence. Do not use it for simple one-shot questions — those just go straight to FINAL:.

**RULE 7 — FINAL ANSWER:**
Only use FINAL: once the entire task is actually done and verified. FINAL: is the marker that ends the turn — use it for the last message of a simple Q&A, or as the closing summary after a string of CONTINUE: updates on a bigger task.

**RULE 8 — NEVER CHAT:**
Do NOT greet the user. Do NOT ask "how can I help you?". Do NOT make small talk. You are an agent — read the task, plan, execute, verify, deliver.

**RULE 9 — PROTECTED TOOLS ARE GATED AUTOMATICALLY:**
The tools install, delete, cleanup, and shell always pause for a human yes/no confirmation — this is enforced by the system itself, not by you. Just call the tool normally when you need it; do not call \'ask\' first for these, and do not stop early to ask the user in plain text — the confirmation prompt will appear on its own. If the human declines, do not retry the same action; propose an alternative or move to FINAL:.
All other tools (read, write, search, mcp, skill, github_*, etc.) run immediately with no confirmation needed — keep working through them without pausing for user input.

**RULE 10 — Projects DIRECTORY:**
All temporary/Projects files MUST go to Projects/ directory.

**RULE 11 — CODE IN YOUR TEXT vs CODE IN A FILE:**
Whenever THINK:, CONTINUE:, or FINAL: contains a SMALL code snippet (roughly under {МАКС_СТРОК_МАЛ_КОД} lines / {МАКС_СИМВ_МАЛ_КОД} characters), wrap it in a normal fenced block: ```language ... ``` exactly as usual — the terminal renderer turns it into a real bordered bubble with syntax colors automatically. Do not try to draw a box yourself.
For LARGE code (a full script, a whole file, anything past that size) — do NOT paste it into THINK:/CONTINUE:/FINAL: text. Instead call TOOL: {{"tool":"write","path":"...","content":"..."}} to put it directly into a file; the terminal will only show a short one-line confirmation, never the full file content. You decide which case applies based on the size of the code you\'re producing. A shell command\'s own output is different — it always prints in its own output bubble, that\'s not affected by this rule.

**RULE 12 — INLINE STYLE MARKUP (CONTINUE/FINAL only):**
You may highlight specific words with `{{{{ц:CODE}}}}text{{{{/ц}}}}` (256-color code, e.g. 208 = orange, 118 = green, 51 = cyan) and make text bold with `{{{{ж}}}}text{{{{/ж}}}}`. Combine bold+color with `{{{{ц:208,ж}}}}text{{{{/ц}}}}`. Use this sparingly, only to draw the eye to something genuinely important (a warning, a key result, a filename) — not on every sentence.

**RULE 13 — PROJECT PLAN MEMORY (build/edit tasks only):**
For substantial project work (building or editing a real project — NOT plain questions, lookups, or chit-chat), the very first time you understand what the project/task needs, call TOOL: {{"tool":"план","action":"сохранить","цель":"<one-line goal>","шаги":[{{"id":"1","текст":"..."}}, ...]}} to persist your understanding to the plan database, keyed to this project folder. On every later request in this project, first call TOOL: {{"tool":"план","action":"получить"}} to recall what you already studied and decided — never re-derive from scratch or contradict a plan you already committed to. When steps complete or the plan changes, call TOOL: {{"tool":"план","action":"обновить","шаги":[...]}} to keep it current. Skip this entirely for ordinary questions, searches, or anything that isn\'t ongoing project construction/editing.

————————————

**OUTPUT FORMAT EXAMPLES:**

THINK: The user wants me to search for the best song by Sherine. I should use the web search tool to find this information.

TOOL: {{"tool":"web_search","query":"best song Sherine Abdel Wahab most popular"}}

[STOP — wait for result]

[After receiving result]

THINK: The search returned several hits. "Masha3er" appears to be the most cited. Let me verify by checking one more source.

TOOL: {{"tool":"web_search","query":"Sherine Masha3er best song reviews"}}

[STOP — wait for result]

[After receiving result]

FINAL: Based on the search results, {{{{ж}}}}"Masha3er" (Feelings){{{{/ж}}}} is widely considered Sherine Abdel Wahab\'s signature and most iconic song...

**Example of a multi-step build task using CONTINUE:**

CONTINUE: Database models are done — moving on to the API routes now.

[work keeps going after this, no stop]

**AVAILABLE TOOLS:**
- read, write, patch, search, list, web_search, shell, install, archive, cleanup, delete, ask
- github_search, github_repo, github_read
- mcp — Call an MCP tool (external server)
- skill — Call a built-in or custom skill
- план — Save/recall/update the persistent project plan (see RULE 13)
- final — Provide final answer (only when done)

**MCP TOOLS:**
Use TOOL: {{"tool":"mcp","mcp_tool":"<tool_name>","arguments":{{...}}}}
{мср_тхт}

**SKILLS:**
Use TOOL: {{"tool":"skill","skill_name":"<skill_name>","arguments":{{...}}}}
{нв_тхт}

**MEMORY CONTEXT:**
{вн_пам}

**WORKSPACE:**
{мф}

**CREATOR:** Dark, independent developer; Telegram: t.me/sii_3
**VERSION:** Released @2026
''';return прм
_МЕТКИ_РЕЖ=['THINK:',_AI,_Ah,_AJ,_AK]
МАКС_СТРОК_МАЛ_КОД=40
МАКС_СИМВ_МАЛ_КОД=800
def _код_маленький(сод):
    if not сод:return _C
    if len(сод)>МАКС_СИМВ_МАЛ_КОД:return _C
    if сод.count(_D)+1>МАКС_СТРОК_МАЛ_КОД:return _C
    return _A
# - By: T.me/sii_3
def _ткст_блок(текст,режим):
    'Пост-обработка целого блока think/continue/final: находит ```код```\n    и рисует настоящий терминальный пузырь вместо сырых ``` fences.\n    Большой код (по решению агента он должен был уйти в файл, а не в чат)\n    не дублируется в терминале целиком — вместо пузыря показывается\n    короткая заметка.';ЗБЛ=re.compile('```[ \\t]*([A-Za-z0-9_+\\-]*)\\n(.*?)```',re.DOTALL);части=[];посл=0
    for m in ЗБЛ.finditer(текст):
        до=текст[посл:m.start()]
        if до.strip() and not до.strip().startswith('```'):
           до = стиль(до) if режим in(_Y, _g) else цв(до, с90, тм=_A)
           части.append(до)
        яз=(m.group(1)or'').strip();код=m.group(2)
        if _код_маленький(код):части.append(_D+пузырь(код,фон=фон_код,подсветка=_A,метка=яз or'code')+_D)
        else:стр_кол=код.count(_D)+1;заметка=f"[{стр_кол} lines / {len(код)} chars omitted from terminal — write large code to a file instead of pasting it here]";части.append(_D+пузырь(заметка,фон=фон_код,подсветка=_C,метка=яз or'code')+_D)
        посл=m.end()
    хвост=текст[посл:]
    if хвост.strip()or not части:хвост=стиль(хвост)if режим in(_Y,_g)else цв(хвост,с90,тм=_A);части.append(хвост)
    return''.join(части)
# - By: T.me/sii_3
_тег_дум_поток=re.compile(r'<\s*/?\s*think(?:ing)?\s*>',re.IGNORECASE)
_тег_поток=('<|tool_call_end|>','<|tool_calls_section_end|>','TOOL:')
# - By: T.me/sii_3
def _без_кавычек(т):
    return str(т).strip().strip('"').strip("'")

def _краткий_путь(путь):
    if not путь:return ''
    п=str(путь).replace('\\','/')
    for пр in ('Projects/grok_extracted/','Projects/','grok_extracted/'):
        if пр in п:return п.split(пр,1)[1]
    return Path(п).name if '/' in п else п

def _сжать_тул(дан):
    дан=str(дан).strip()
    if not дан:return ''
    if '\n' in дан or '&&' in дан or '||' in дан or ';' in дан or '|' in дан:return ''
    н=дан.lower()
    if н.startswith('cat '):
        return f"Cat {_краткий_путь(_без_кавычек(дан[4:]))}"
    if н.startswith('ls ') or н.startswith('list '):
        return f"List {_краткий_путь(_без_кавычек(дан.split(None,1)[1]))}"
    return ''

def _сжать_думку(текст):
    if not текст:return ''
    текст=_тег_дум_поток.sub('',str(текст))
    out=[];i=0;L=len(текст)
    while i<L:
        j=текст.find(_AI,i)
        if j==-1:
            out.append(текст[i:]);break
        out.append(текст[i:j])
        k=j+len(_AI)
        while k<L and текст[k].isspace():k+=1
        if k>=L or текст[k] != '{':
            i=k;continue
        brace=0;ins=False;esc=False;end=None
        for m in range(k,L):
            ch=текст[m]
            if esc:esc=False;continue
            if ch=='\\':esc=True;continue
            if ch=='"' and not esc:ins=not ins;continue
            if not ins:
                if ch=='{':brace+=1
                elif ch=='}':
                    brace-=1
                    if brace==0:
                        end=m+1;break
        if end is None:
            i=k;continue
        raw=текст[k:end]
        try:obj=json.loads(raw)
        except Exception:
            i=end;continue
        if isinstance(obj,dict):
            tool=str(obj.get('tool') or obj.get('action') or obj.get('command_name') or '').lower()
            if tool=='shell':
                cmd=str(obj.get('command') or obj.get('cmd') or obj.get('rcommand') or '').strip()
                summ=_сжать_тул(cmd)
                if summ:out.append(summ)
            elif tool in ('list','ls','read','cat','show'):
                p=str(obj.get('path') or obj.get('file') or obj.get('target') or '')
                if tool in ('list','ls'):out.append(f"List {_краткий_путь(p)}".strip())
                else:out.append(f"Cat {_краткий_путь(p)}".strip())
            elif tool in ('archive','extract'):
                src=_краткий_путь(obj.get('source') or obj.get('file') or '')
                tgt=_краткий_путь(obj.get('target') or obj.get('path') or '')
                if src or tgt:out.append(f"Extract {src} -> {tgt}".strip())
            elif tool in ('write','edit','replace','patch'):
                p=_краткий_путь(obj.get('path') or obj.get('file') or obj.get('target') or '')
                if p:out.append(f"Edit {p}")
        i=end
    return ''.join(out)

def _очистить_поток(текст):
    if not текст:
        return ''
    return _сжать_думку(текст)
# - By: T.me/sii_3
def рп(кус, ст):
    ст.setdefault(_Z, ''); ст.setdefault(_H, ''); ст.setdefault(_f, _A)
    ст.setdefault(_R, ''); ст.setdefault(_A2, _C); ст.setdefault(_S, '')
    ст.setdefault(_AG, ''); ст.setdefault(_AH, 0); ст.setdefault('первый_вывод', _C)
    ст[_Z] += кус
    ожд = ст[_Z]
    while ожд:
        if ст[_f]:
            совп = _C
            for лбл in _МЕТКИ_РЕЖ:
                if ожд.startswith(лбл):
                    if ст[_H] and ст[_S] is not _B:
                        _флш_блок(ст)
                    ожд = ожд[len(лбл):]
                    ст[_H] = лбл[:-1].lower()
                    ст[_f] = _C
                    ст[_A2] = _C
                    ст[_S] = ''
                    if ст[_H] == _t:
                        ст[_R] = ''
                    совп = _A
                    break
            if совп:
                continue
            if any(лбл.startswith(ожд) for лбл in _МЕТКИ_РЕЖ):
                break
        ch = ожд[0]
        ожд = ожд[1:]
        if ch == _D:
            ст[_f] = _A
        if ст[_H] == _Y or ст[_H] == _g:
            ch = _очистить_поток(ch)
            if not ch:
                continue
            if not ст['первый_вывод'] and ch.strip():
                ch = ch.lstrip()
                ст['первый_вывод'] = _A
            sys.stdout.write(ch)
            sys.stdout.flush()
            ст[_S] += ch
            continue
        if ст[_H] == _t:
            ст[_R] += ch
            if ст[_f] or len(ст[_R]) > 50:
                parsed = пж(ст[_R])
                if parsed is not _B:
                    if 'tool' in parsed or 'action' in parsed:
                        ст[_Z] = ожд
                        return _A
            continue
        if ст[_H] == _AW:
            ch = _очистить_поток(ch)
            if not ch:
                continue
            if not ст['первый_вывод'] and ch.strip():
                ch = ch.lstrip()
                ст['первый_вывод'] = _A
            ст[_AG] += ch
            sys.stdout.write(цв(ch, с90, тм=_A))
            sys.stdout.flush()
            ст[_AH] += 1
            continue
        if ст[_H] == 'progress':
            ch = _очистить_поток(ch)
            if not ch:
                continue
            if not ст['первый_вывод'] and ch.strip():
                ch = ch.lstrip()
                ст['первый_вывод'] = _A
            sys.stdout.write(цв(ch, с208))
            sys.stdout.flush()
            continue
        if not ст[_H]:
            ch = _очистить_поток(ch)
            if not ch:
                continue
            if not ст['первый_вывод'] and ch.strip():
                ch = ch.lstrip()
                ст['первый_вывод'] = _A
            sys.stdout.write(ch)
            sys.stdout.flush()
    ст[_Z] = ожд
    if ст[_H] == _t and ст[_R]:
        parsed = пж(ст[_R])
        if parsed is not _B:
            return _A
    return _C
def _флш_блок(ст):
    if ст[_H] in (_Y, _g) and ст[_S].strip():
        готово = _ткст_блок(_сжать_думку(ст[_S]), ст[_H])
        sys.stdout.write(готово)
        sys.stdout.write(_A1)
        sys.stdout.flush()
    elif ст[_H] == _AW:
        sys.stdout.write(_A1)
        sys.stdout.flush()
    ст[_S] = ''
def _фон_план(сес,ткн,мдл,смс_копия,вп,проект):
    'Второй, параллельный запрос к модели — работает в фоновом потоке\n    одновременно с основным (видимым) запросом THINK/TOOL/FINAL.\n    Этот запрос не показывается пользователю: он просит модель выдать\n    ПОЛНЫЙ план (цель + шаги) в чистом JSON, и результат сохраняется в\n    таблицу планы_пр (через Вп.сохр_план/обн_план) — план живёт в БД\n    временно, пока проект не завершится (см. завершить_план в главном\n    цикле при FINAL).'
    try:
        сис_план='You are a silent planning assistant running in the background. Do not chat, do not explain. Read the conversation so far and output ONLY a JSON object — nothing else, no markdown fences — with this exact shape: {"цель": "<one-line goal of the current project/task>", "шаги": [{"id": "1", "текст": "<step>"}, ...]}. Keep it a real, complete, detailed plan (this is the FULL internal plan, not the short version shown on screen).';смс_план=[{_F:_P,_E:сис_план}]+смс_копия[-12:];текст=''.join(по(сес,ткн,мдл,смс_план)).strip();д=пж(текст)
        if not д:return
        цель=str(д.get(_a)or д.get('goal')or'').strip();шаги=д.get(_T)or д.get(_AV)or[]
        if not цель:return
        сущ=вп.план_проекта(проект)
        if сущ:вп.обн_план(сущ[_I],шаги,заметки=цель)
        else:вп.сохр_план(проект,цель,шаги)
    except Exception:pass
def _завершить_если_план(вп,проект):
    'Когда проект/задача реально завершена (FINAL), временный план,\n    хранившийся в БД, помечается как готовый — он не растёт бесконечно.'
    try:
        сущ=вп.план_проекта(проект)
        if сущ:вп.завершить_план(сущ[_I])
    except Exception:pass
def глв():
    пам=Вп();поиск=Поиск();мдл=вм()
    кр,ист,ист_ф=вп();пф=Пф(кр);print(цв(f"\nProject Folder: {кр}",сз,ж=_A))
    if ист_ф is not _B and ист_ф.suffix.lower()=='.zip':print(цв('-- Archive extracted',сз))
    print(цв('\n○ Build MCP...',сг,тм=_A));мср=McpMgr();мср_кол=len(мср.список())
    if мср_кол>0:print(цв(f"\n- MCP: {мср_кол} tools",сз))
    else:print(цв('-- MCP Not Found :|\n',с90,тм=_A))
    нвр=НвкРег();нв_кол=len(нвр.список());print(цв(f"- Skills: {нв_кол} ready >_\n\n",сз));сес=requests.Session();сес.headers.update(зг());ткн,_п_id=рг(сес);сис_пр=сисп(кр,ист,ист_ф,мср,нвр,пам,пф);смс=[{_F:_P,_E:сис_пр}];print(цв('☆ - Enter Prompt - "exit" To Quit',с90,тм=_A))
    while _A:
        try:пт=input(цв('> ',сж)).rstrip()
        except(EOFError,KeyboardInterrupt):print("\n");break
        if not пт:continue
        if пт.lower()in{'exit','quit'}:break
        низ=пт.lower()
        if низ=='mcp status':
            инс=мср.список();print(цв(f"MCP servers: {len(мср.серв)} | Tools: {len(инс)}",сг,ж=_A))
            for т in инс:print(цв(f"  - {т[_N]}",сб))
            continue
        if низ=='skills':
            нв=нвр.список();print(цв(f"Skills: {len(нв)}",сг,ж=_A))
            for н in нв:print(цв(f"  - {н.им}: {н.оп}",сб))
            continue
        if низ=='status':print(цв('System active',сб));continue
        if низ=='context':print(цв('Context printed',сб));continue
        if низ=='search_test':
            print(цв('— Search Test...',сг));р=поиск.ищи('test query',3);print(цв(f"Result: {р.get(_K,_C)} | Engine: {р.get(_k,"нет")}",сз))
            if р.get(_U):
                for(i,э)in enumerate(р[_U][:3]):print(цв(f"  {i+1}. {э.get("title","N/A")[:60]}",сб))
            continue
        смс.append({_F:'user',_E:пт});смс=ск(смс,макс=200000);print(_A1,end='');threading.Thread(target=_фон_план,args=(сес,ткн,мдл,list(смс),пам,str(кр)),daemon=_A).start()
        for _ in range(24):
            аст='';пот_ст={_Z:'',_H:'',_f:_A,_R:'',_S:'',_AG:'',_AH:0,_A2:_C};инс_найд=_C
            try:
                for кус in по(сес,ткн,мдл,смс):
                    аст+=кус
                    if not инс_найд:
                        if рп(кус,пот_ст):инс_найд=_A
            except Exception as e:print(цв(f"Error: {e}",ср,ж=_A));break
            plain_streamed=bool(пот_ст.get(_H));блок_уже_напечатан=not инс_найд
            if блок_уже_напечатан:_флш_блок(пот_ст)
            пот_ст[_Z]='';инс_нг,фнл_тхт,мсл_тхт,прод_тхт=пп(аст)
            if инс_нг is not _B:
                инс=ии(инс_нг)
                if инс==_X:
                    сдр=фнл_тхт or str(инс_нг.get(_E)or инс_нг.get(_Y)or'').strip();смс.append({_F:_O,_E:аст})
                    if сдр:print(_ткст_блок(сдр,_Y))
                    print(_D,end='');_завершить_если_план(пам,str(кр));break
                if инс in опасные_инстр:
                    if not эизн(инс,инс_нг):инс_им,рзт=инс,'User declined this action. Do not retry it; ask for an alternative approach or continue with FINAL: if nothing else is needed.'
                    else:инс_им,рзт=ви(кр,инс_нг,мср,нвр,пам,пф)
                else:инс_им,рзт=ви(кр,инс_нг,мср,нвр,пам,пф)
                if инс_им==_Q:print(пузырь(рзт,фон=фон_вывод,подсветка=_C,метка='output'))
                elif инс_им==_e:print(пузырь(рзт,фон=фон_вывод,подсветка=_C,метка='install'))
                elif инс_им in(_x,_AB):
                    сод_written = str(инс_нг.get(_E, '')) if инс_им == _x else ''
                    пт_written = str(инс_нг.get(_AE) or инс_нг.get(_AF) or инс_нг.get(_AU) or '')
                    метка_файла = Path(пт_written).name if пт_written else 'code'
                    if сод_written and _код_маленький(сод_written):
                        print(пузырь(сод_written, фон=фон_код, подсветка=_A, метка=метка_файла))
                    else:
                        print(цв(рзт, сз))
                elif инс_им in(_AC,_d,_A9,_AA,_s,_v,_w):0
                else:0
                print(_D,end='');смс.append({_F:_O,_E:аст});смс.append({_F:'user',_E:f"результат {инс_им}:\n{рзт}"});смс=ск(смс,макс=200000);continue
            if фнл_тхт:
                смс.append({_F:_O,_E:аст})
                if not блок_уже_напечатан:print(_D,end='')
                _завершить_если_план(пам,str(кр));break
            if прод_тхт:смс.append({_F:_O,_E:аст});смс=ск(смс,макс=200000);continue
            if мсл_тхт:смс.append({_F:_O,_E:аст});смс.append({_F:_P,_E:'You only thought — you have not acted yet. Send another response now: THINK: to reason further, TOOL: to use a tool, CONTINUE: for a visible progress update, or FINAL: to answer. Pick exactly one.'});смс=ск(смс,макс=200000);continue
            чист_аст=без_нативн_думания(аст)
            if not чист_аст:смс.append({_F:_O,_E:аст});смс.append({_F:_P,_E:'You only produced internal reasoning and stopped without a TOOL:, CONTINUE:, or FINAL: marker. Continue now — output TOOL: with a JSON tool call, CONTINUE: for a progress update, or FINAL: with your answer.'});смс=ск(смс,макс=200000);continue
            if not plain_streamed:смс.append({_F:_O,_E:аст});print(_ткст_блок(_очистить_поток(чист_аст),_Y),end=_A1 if not чист_аст.endswith(_D)else _D,flush=_A);break
            if plain_streamed:
                смс.append({_F:_O,_E:аст})
                if not блок_уже_напечатан:print(_D,end='')
                break
            print(цв('- No response',ср,ж=_A));print(_A1,end='');break
        else:print(цв('\n-- Stopped after 24 steps without a final answer.',сж,ж=_A))
    мср.стоп_все();print(цв('Fack You - [ Bye 👋 ] -_-\n',сз,ж=_A))
main=глв
if __name__=='__main__':глв()

# - By: T.me/sii_3

