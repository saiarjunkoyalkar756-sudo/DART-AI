from __future__ import annotations

__all__ = ["пуск"]

def пуск(*args, **kwargs):
    from .режим import пуск as _пуск
    return _пуск(*args, **kwargs)