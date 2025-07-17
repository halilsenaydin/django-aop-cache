from abc import ABC, abstractmethod
from typing import Callable
from core.messaging.config import ExchangeConfig


class MessageBroker(ABC):
    @abstractmethod
    def publish(self, config: ExchangeConfig, payload: dict):
        pass

    @abstractmethod
    def declare_exchange(self, config: ExchangeConfig):
        pass

    @abstractmethod
    def consume(self, config: ExchangeConfig, queue_name: str, callback: Callable):
        pass
