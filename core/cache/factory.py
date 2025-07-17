from threading import Lock
from core.cache.cache_handler import CacheHandler
from core.cache.cache_manager import CacheManager
from core.cache.redis_cache_manager import RedisCacheManager


class CacheManagerFactory:
    _instance = None
    _lock = Lock()

    @classmethod
    def get_instance(cls) -> CacheManager:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = RedisCacheManager()

        return cls._instance


class CacheHandlerFactory:
    _instance = None
    _lock = Lock()

    @classmethod
    def get_instance(cls) -> CacheHandler:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = CacheHandler()

        return cls._instance
