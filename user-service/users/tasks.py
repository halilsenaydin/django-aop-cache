"""
Publishes user update events to the message broker.

This module is responsible for formatting and sending user-related events
(e.g., created, updated, or group-changed) to a message broker using a fanout exchange.
These events can be consumed by other services to stay in sync with user data.

The event follows a structured JSON message format and is sent using the
MessageBrokerFactory abstraction to support RabbitMQ, Kafka, etc.
"""

from core.messaging.factory import MessageBrokerFactory
from core.messaging.config import ExchangeConfig


def publish_user_updated_event(user):
    """
    Publishes a 'user.updated' event to the message broker with the given user data.

    The message is published to the 'user_events' fanout exchange,
    allowing multiple services to listen for user update notifications.

    Parameters:
        user (dict): A dictionary containing user fields, such as id, username, email, etc.
                     It may also include keys like 'created' or 'deleted' depending on context.
    """

    # Create payload
    user_data = {
        "id": user.get("id"),
        "username": user.get("username"),
        "email": user.get("email"),
        "first_name": user.get("first_name"),
        "last_name": user.get("last_name"),
        "is_active": user.get("is_active"),
        "groups": user.get("groups"),
    }
    message = {
        "event": "user.updated",
        "user": user_data,
        "created": user.get("created"),
    }

    # Publish to broker
    config = ExchangeConfig(
        name="user_events",
        type="fanout",
        durable=True,
        auto_delete=False,
        routing_key="",
    )
    broker = MessageBrokerFactory.get_instance()

    broker.publish(config, message)
