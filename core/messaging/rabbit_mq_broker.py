import json
import pika
from typing import Callable
from contextlib import contextmanager
from core.constants import ConfigConstant
from core.messaging.message_broker import MessageBroker
from core.messaging.config import ExchangeConfig


class RabbitMqBroker(MessageBroker):
    HOST = ConfigConstant.RABBITMQ_HOST
    PORT = ConfigConstant.RABBITMQ_PORT
    USER = ConfigConstant.RABBITMQ_USER
    PASS = ConfigConstant.RABBITMQ_PASS

    @contextmanager
    def _connection_channel(self):
        credentials = pika.PlainCredentials(self.USER, self.PASS)
        parameters = pika.ConnectionParameters(
            host=self.HOST,
            port=self.PORT,
            virtual_host="/",
            credentials=credentials,
        )
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        try:
            yield channel
        finally:
            connection.close()

    def _setup_exchange_and_queue(
        self, channel, config: ExchangeConfig, queue_name: str = None
    ):
        channel.exchange_declare(
            exchange=config.name,
            exchange_type=config.type,
            durable=config.durable,
            auto_delete=config.auto_delete,
        )

        if queue_name:
            channel.queue_declare(queue=queue_name, durable=True)
            channel.queue_bind(
                exchange=config.name, queue=queue_name, routing_key=config.routing_key
            )

    def declare_exchange(self, config: ExchangeConfig):
        with self._connection_channel() as channel:
            self._setup_exchange_and_queue(channel, config)

    def publish(self, config: ExchangeConfig, payload: dict):
        with self._connection_channel() as channel:
            self._setup_exchange_and_queue(channel, config)
            channel.basic_publish(
                exchange=config.name,
                routing_key=config.routing_key,
                body=json.dumps(payload),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    content_type="application/json",
                ),
            )

    def consume(self, config: ExchangeConfig, queue_name: str, callback: Callable):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.HOST,
                port=self.PORT,
                virtual_host="/",
                credentials=pika.PlainCredentials(self.USER, self.PASS),
            )
        )
        channel = connection.channel()

        self._setup_exchange_and_queue(channel, config, queue_name)
        channel.basic_qos(prefetch_count=config.prefetch_count)
        channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=config.auto_ack,
        )

        print(f"[x] Listening on queue '{queue_name}'...")

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            print("[!] Consuming stopped by user.")

            channel.stop_consuming()
        finally:
            connection.close()
