from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict


@dataclass
class CacheKeyMeta:
    service: str
    app: str
    model: str


@dataclass
class ModelCacheKeyMeta(CacheKeyMeta):
    obj_id: int


@dataclass
class EndpointCacheKeyMeta(CacheKeyMeta):
    endpoint: str
    query_params: Dict[str, str]


class CacheManager(ABC):
    @abstractmethod
    def get(self, key: str) -> str | None:
        pass

    @abstractmethod
    def set(self, key: str, value: str, ex: int = None) -> None:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass

    @abstractmethod
    def delete_pattern(self, pattern: str) -> None:
        pass

    @abstractmethod
    def generate_model_key(self, meta: ModelCacheKeyMeta) -> str:
        pass

    @abstractmethod
    def generate_endpoint_key(self, meta: EndpointCacheKeyMeta) -> str:
        pass
