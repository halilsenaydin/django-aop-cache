from urllib.parse import urlencode
import hashlib
from django_redis import get_redis_connection
from core.cache.cache_manager import CacheManager
from core.cache.cache_manager import ModelCacheKeyMeta, EndpointCacheKeyMeta
from core.constants import CacheConstant


class RedisCacheManager(CacheManager):
    def __init__(self, alias="default"):
        self.redis = get_redis_connection(alias)

    def get(self, key: str) -> str | None:
        value = self.redis.get(key)

        if value is not None:
            return value.decode("utf-8")

        return None

    def set(self, key: str, value: str, ex: int = CacheConstant.TIMEOUT) -> None:
        self.redis.set(key, value, ex=ex)

    def delete(self, key: str) -> None:
        self.redis.delete(key)

    def delete_pattern(self, pattern: str) -> None:
        cursor = 0

        while True:
            cursor, keys = self.redis.scan(cursor=cursor, match=pattern, count=1000)

            if keys:
                pipeline = self.redis.pipeline()
                for key in keys:
                    pipeline.unlink(key)
                pipeline.execute()

            if cursor == 0:
                break

    def generate_model_key(self, meta: ModelCacheKeyMeta) -> str:
        return f"{meta.service}{CacheConstant.SEPERATOR}{meta.app}{CacheConstant.SEPERATOR}{meta.model}{CacheConstant.SEPERATOR}{CacheConstant.TYPE_MODEL}{CacheConstant.SEPERATOR}{meta.obj_id}"

    def generate_endpoint_key(self, meta: EndpointCacheKeyMeta) -> str:
        query_string = urlencode(sorted(meta.query_params.items()))
        query_hash = hashlib.md5(query_string.encode()).hexdigest()

        return f"{meta.service}{CacheConstant.SEPERATOR}{meta.app}{CacheConstant.SEPERATOR}{meta.model}{CacheConstant.SEPERATOR}{CacheConstant.TYPE_ENDPOINT}{CacheConstant.SEPERATOR}{meta.endpoint}{CacheConstant.SEPERATOR}{query_hash}"
