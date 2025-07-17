from celery import shared_task
from core.utils import CacheUtil


@shared_task
def cache_delete_pattern(pattern: str):
    cache_manager = CacheUtil.get_cache_manager()

    cache_manager.delete_pattern(pattern)
