from contextlib import contextmanager
import threading


class CacheContext:
    _local = threading.local()

    CONTEXT_FROM_VIEW = "from_view"

    @classmethod
    def set(cls, key: str, value: any):
        setattr(cls._local, key, value)

    @classmethod
    def get(cls, key: str, default=None):
        return getattr(cls._local, key, default)

    @classmethod
    def reset(cls, key: str):
        if hasattr(cls._local, key):
            delattr(cls._local, key)

    @classmethod
    def clear(cls):
        cls._local.__dict__.clear()
