from functools import wraps
import json
from rest_framework.response import Response
from core.cache.cache_manager import EndpointCacheKeyMeta
from core.constants import ErrorConstant, CacheConstant
from core.context.cache_context import CacheContext
from core.utils import CacheUtil


def cacheable(
    type: str = None,
    source: str = CacheConstant.SOURCE_VIEW_MODEL_VIEW_SET,
    timeout: int = CacheConstant.TIMEOUT,
):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            key_meta = CacheUtil.get_key_meta(self, source)

            if not key_meta:
                return self.error_response(
                    status_code=ErrorConstant.INTERNAL_SERVER_ERROR
                )

            cache_manager = CacheUtil.get_cache_manager()

            if type == CacheConstant.TYPE_MODEL:
                pk = kwargs.get("pk")
                meta = CacheUtil.generate_model_cache_key_meta(key_meta, pk)
                key = cache_manager.generate_model_key(meta)
            elif type == CacheConstant.TYPE_ENDPOINT:
                meta = EndpointCacheKeyMeta(
                    service=key_meta.service,
                    app=key_meta.app,
                    model=key_meta.model,
                    endpoint=func.__name__,
                    query_params=request.query_params.dict(),
                )
                key = cache_manager.generate_endpoint_key(meta)
            else:
                key = None

            cached_data = cache_manager.get(key)

            if cached_data:
                encoded_data = json.loads(cached_data)

                return self.success_data_response(encoded_data)

            response = func(self, request, *args, **kwargs)

            if isinstance(response, Response) and response.status_code == 200:
                json_data = json.dumps(response.data.get("data"))

                cache_manager.set(key, json_data, timeout)

            return response

        return wrapper

    return decorator


def cache_update(
    source=CacheConstant.SOURCE_VIEW_MODEL_VIEW_SET,
    timeout=CacheConstant.TIMEOUT,
    data_getter=None,
    service_name=None,
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            status, response, meta, data = CacheUtil.process_cache_action(
                func, args, kwargs, source, service_name, data_getter
            )

            if not status:
                return response if CacheUtil.is_view(source) else func(*args, **kwargs)

            cache_handler = CacheUtil.get_cache_handler()
            cache_handler.cache_update(meta, data, timeout)

            CacheContext.reset(CacheContext.CONTEXT_FROM_VIEW)

            return response if CacheUtil.is_view(source) else func(*args, **kwargs)

        return wrapper

    return decorator


def cache_invalidate(
    type=None, source=CacheConstant.SOURCE_VIEW_MODEL_VIEW_SET, service_name=None
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            status, response, meta, _ = CacheUtil.process_cache_action(
                func, args, kwargs, source, service_name
            )

            if not status:
                return response if CacheUtil.is_view(source) else func(*args, **kwargs)

            cache_handler = CacheUtil.get_cache_handler()
            cache_handler.cache_invalidate(type, meta)

            CacheContext.reset(CacheContext.CONTEXT_FROM_VIEW)

            return response if CacheUtil.is_view(source) else func(*args, **kwargs)

        return wrapper

    return decorator
