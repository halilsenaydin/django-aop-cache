import json
from core.cache.cache_manager import CacheKeyMeta
from core.constants import CacheConstant
from core.tasks import cache_delete_pattern
from core.utils import CacheUtil


class CacheHandler:
    def __init__(self):
        self.cache_manager = CacheUtil.get_cache_manager()

    def cache_update(
        self,
        meta: CacheKeyMeta,
        data: any,
        timeout: int = CacheConstant.TIMEOUT,
    ):
        # Delete endpoint caches
        pattern = f"{meta.service}{CacheConstant.SEPERATOR}{meta.app}{CacheConstant.SEPERATOR}{meta.model}{CacheConstant.SEPERATOR}{CacheConstant.TYPE_ENDPOINT}{CacheConstant.SEPERATOR}*"

        cache_delete_pattern.delay(pattern)

        key = self.cache_manager.generate_model_key(meta)

        json_data = json.dumps(data)
        self.cache_manager.set(key, json_data, timeout)

    def cache_invalidate(self, type: str, meta: CacheKeyMeta):
        if type == CacheConstant.TYPE_MODEL:
            key = self.cache_manager.generate_model_key(meta)

            self.cache_manager.delete(key)

        pattern = f"{meta.service}{CacheConstant.SEPERATOR}{meta.app}{CacheConstant.SEPERATOR}{meta.model}{CacheConstant.SEPERATOR}{CacheConstant.TYPE_ENDPOINT}{CacheConstant.SEPERATOR}*"

        cache_delete_pattern.delay(pattern)
