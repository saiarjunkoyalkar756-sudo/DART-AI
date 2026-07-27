# - @2026 | Version 2.0
# - Created By: T.me/sii_3
# - Mr Dark

# ~ Agent DarkPs Official [>_]

from __future__ import annotations

import subprocess
import sys
import json


def запрос(сс, ткн, мдл, смс):
    процесс = subprocess.Popen(
        [sys.executable, "api.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    вход = {
        "model": мдл,
        "messages": смс,
    }

    процесс.stdin.write(
        json.dumps(вход, ensure_ascii=False) + "\n"
    )
    процесс.stdin.flush()
    процесс.stdin.close()

    первый_выход = True
    последнее = None

    for строка in процесс.stdout:
        строка = строка.rstrip("\n\r")

        if not строка:
            continue

        try:
            данные = json.loads(строка)

            if isinstance(данные, dict):
                тип = str(данные.get("тип") or данные.get("type") or "").strip().lower()
                текст = данные.get("текст")
                if текст is None:
                    текст = данные.get("text")

                if not текст:
                    continue

                chunk = str(текст)
                норм = chunk.strip()
                if not норм or норм == последнее:
                    continue
                последнее = норм

                if первый_выход:
                    chunk = "\n\n" + chunk.lstrip(" \t")
                    первый_выход = False

                yield chunk
                continue

        except Exception:
            pass

        if строка.startswith(("API ", "MODEL:", "MESSAGES:", "STATUS:")):
            continue

        норм = строка.strip()
        if not норм or норм == последнее:
            continue
        последнее = норм

        if первый_выход:
            yield "\n\n" + строка.lstrip(" \t")
            первый_выход = False
        else:
            yield строка

    процесс.wait()

# - By: T.me/sii_3