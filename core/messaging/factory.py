from core.messaging.rabbit_mq_broker import RabbitMqBroker
from threading import Lock


class MessageBrokerFactory:
    _instance = None
    _lock = Lock()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = RabbitMqBroker()

        return cls._instance
