import json, jwt, pika, requests
from typing import Optional, Callable
from django.conf import settings
from rest_framework.response import Response
from core.constants import MessageConstant, CacheConstant, ConfigConstant
from core.context.cache_context import CacheContext
from core.cache.cache_manager import CacheKeyMeta, ModelCacheKeyMeta


class CacheUtil:
    @staticmethod
    def get_cache_manager():
        from core.cache.factory import CacheManagerFactory

        return CacheManagerFactory.get_instance()

    @staticmethod
    def get_cache_handler():
        from core.cache.factory import CacheHandlerFactory

        return CacheHandlerFactory.get_instance()

    @staticmethod
    def get_service_from_self(self):
        service = getattr(self, "cache_service_name", None)

        return service

    @staticmethod
    def get_obj_id(data_source, kwargs):
        if "pk" in kwargs:
            return kwargs["pk"]

        if hasattr(data_source, "pk"):
            return data_source.pk

        if hasattr(data_source, "id"):
            return data_source.id

        return None

    @staticmethod
    def process_view_source(func, args, kwargs, expected_statuses, source):
        status, response, data_source, _, key_meta = CacheUtil.handle_view(
            func, args, kwargs, expected_statuses, source
        )

        if not status:
            return False, response, None, None

        obj_id = CacheUtil.get_obj_id(data_source, kwargs)

        return True, response, key_meta, obj_id

    @staticmethod
    def process_signal_source(func, args, kwargs, service_name, data_getter):
        status, signal, data_source, _, key_meta = CacheUtil.handle_signal(
            func, args, kwargs, service_name, data_getter
        )

        if not status:
            return False, signal, None, None

        obj_id = CacheUtil.get_obj_id(data_source, {})

        return True, signal, key_meta, obj_id, data_source

    @staticmethod
    def process_cache_action(
        func,
        args,
        kwargs,
        source,
        service_name=None,
        data_getter=None,
        expected_statuses=(200, 201, 204),
    ):
        if CacheUtil.is_view(source):
            status, response, key_meta, obj_id = CacheUtil.process_view_source(
                func, args, kwargs, expected_statuses, source
            )
            if not status:
                return False, response, None, None

            data = None
        elif source == CacheConstant.SOURCE_SIGNAL:
            status, signal, key_meta, obj_id, data_source = (
                CacheUtil.process_signal_source(
                    func, args, kwargs, service_name, data_getter
                )
            )

            if not status:
                return False, signal, None, None

            data = data_source if data_getter is None else data_getter(data_source)
        else:
            return False, func(*args, **kwargs), None, None

        if not all([key_meta, obj_id]):
            return False, None, None, None

        meta = CacheUtil.generate_model_cache_key_meta(key_meta, obj_id)

        return True, None, meta, data

    @staticmethod
    def get_key_meta(
        data_source: any, source: str, service_getter: Callable = get_service_from_self
    ) -> CacheKeyMeta | None:
        if source == CacheConstant.SOURCE_VIEW_MODEL_VIEW_SET:
            service = service_getter(data_source)
            queryset = getattr(data_source, "queryset", None)
            model = getattr(queryset, "model", None)

        elif source == CacheConstant.SOURCE_SIGNAL:
            service = service_getter()
            model = data_source

        app = model._meta.app_label
        model_name = model._meta.model_name

        if not all([service, app, model]):
            return None

        return CacheKeyMeta(service, app, model_name)

    @staticmethod
    def generate_model_cache_key_meta(
        key_meta: CacheKeyMeta, obj_id: str
    ) -> ModelCacheKeyMeta:
        return ModelCacheKeyMeta(
            service=key_meta.service,
            app=key_meta.app,
            model=key_meta.model,
            obj_id=obj_id,
        )

    @staticmethod
    def handle_signal(
        func,
        args,
        kwargs,
        service_name: str,
        data_getter: Callable = lambda data: data,
        source: str = CacheConstant.SOURCE_SIGNAL,
    ):
        if CacheContext.get(CacheContext.CONTEXT_FROM_VIEW):
            CacheContext.reset(CacheContext.CONTEXT_FROM_VIEW)

            return False, func(*args, **kwargs), None, None, None

        instance = kwargs.get("instance") or (args[1] if len(args) > 1 else None)

        if not instance:
            return False, func(*args, **kwargs), None, None, None

        data = data_getter(instance)
        key_meta = CacheUtil.get_key_meta(instance, source, lambda: service_name)

        return True, None, instance, data, key_meta

    @staticmethod
    def handle_view(
        func,
        args,
        kwargs,
        status_codes=(200, 201, 204),
        source=CacheConstant.SOURCE_VIEW_MODEL_VIEW_SET,
    ):
        CacheContext.set(CacheContext.CONTEXT_FROM_VIEW, True)

        response = func(*args, **kwargs)

        if (
            not isinstance(response, Response)
            or response.status_code not in status_codes
        ):
            return False, response, None, None, None

        self = args[0]

        if not self:
            return False, response, None, None, None

        data = getattr(response, "data", {}).get("data")
        key_meta = CacheUtil.get_key_meta(self, source)

        return True, response, self, data, key_meta

    @staticmethod
    def is_view(source: str) -> bool:
        return (
            source == CacheConstant.SOURCE_VIEW_MODEL_VIEW_SET
            or source == CacheConstant.SOURCE_VIEW_API_VIEW
        )


class HttpUtil:
    @staticmethod
    def set_auth_header(headers: dict = None, token: str = None):
        if headers is None:
            headers = {}

        if token:
            headers["Authorization"] = f"Bearer {token}"

        return headers

    @staticmethod
    def get(url: str, params: dict = None, timeout: int = 3, headers: dict = None):
        """
        Sends a GET request to the specified URL with optional query parameters, headers, and timeout.

        Args:
            url (str): The target URL for the GET request.
            params (dict, optional): Dictionary of query string parameters to append to the URL. Defaults to None.
            timeout (int, optional): Timeout duration in seconds for the request. Defaults to 3.
            headers (dict, optional): HTTP headers to include in the request. Defaults to None.

        Returns:
            tuple: (response_json, error_message)
                - response_json (dict or list): Parsed JSON response if successful; otherwise None.
                - error_message (str or None): Error message string if an error occurred; otherwise None.
        """
        try:
            response = requests.get(
                url, params=params, timeout=timeout, headers=headers
            )

            response.raise_for_status()

            return response.json(), None
        except requests.RequestException as e:
            return None, MessageConstant.ERROR_SERVICE_REQUEST

    @staticmethod
    def post(url: str, payload: dict = None, timeout: int = 3, headers: dict = None):
        """
        Sends a POST request to the specified URL with optional JSON payload, headers, and timeout.

        Args:
            url (str): The target URL for the POST request.
            payload (dict, optional): JSON-serializable dictionary to send as the request body. Defaults to None.
            timeout (int, optional): Timeout duration in seconds for the request. Defaults to 3.
            headers (dict, optional): HTTP headers to include in the request. Defaults to None.

        Returns:
            tuple: (response_json, error_message)
                - response_json (dict or list): Parsed JSON response if successful; otherwise None.
                - error_message (str or None): Error message string if an error occurred; otherwise None.
        """
        try:
            response = requests.post(
                url, json=payload, timeout=timeout, headers=headers
            )

            response.raise_for_status()

            return response.json(), None
        except requests.RequestException as e:
            # if hasattr(e, "response") and e.response is not None:
            #     error_html = e.response.text
            #     with open("error_response.html", "w", encoding="utf-8") as f:
            #         f.write(error_html)

            return None, MessageConstant.ERROR_SERVICE_REQUEST


class JwtUtil:
    @staticmethod
    def get_token(headers: dict) -> Optional[str]:
        """
        Extracts the JWT token from the Authorization header.

        Args:
            headers (dict): HTTP headers dictionary (typically request.headers)

        Returns:
            Optional[str]: The JWT token if present and well-formed, otherwise None.

        Notes:
            Expects the header in the format: 'Authorization: Bearer <token>'.
            If header is missing or malformed, returns None.
        """
        authorization = headers.get("Authorization")

        if not authorization or not authorization.startswith("Bearer "):
            return None

        parts = authorization.split(" ", 1)

        return parts[1] if len(parts) == 2 else None

    @staticmethod
    def get_token_payload(token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            return payload
        except (jwt.DecodeError, jwt.ExpiredSignatureError, AttributeError):
            return None


class RabbitMqUtil:
    DEFAULT_EXCHANGE = "user_events"
    DEFAULT_EXCHANGE_TYPE = "fanout"
    DEFAULT_HOST = ConfigConstant.RABBITMQ_HOST
    DEFAULT_PORT = ConfigConstant.RABBITMQ_PORT
    DEFAULT_USERNAME = ConfigConstant.RABBITMQ_USER
    DEFAULT_PASSWORD = ConfigConstant.RABBITMQ_PASS

    @staticmethod
    def get_connection():
        credentials = pika.PlainCredentials(
            RabbitMqUtil.DEFAULT_USERNAME, RabbitMqUtil.DEFAULT_PASSWORD
        )
        parameters = pika.ConnectionParameters(
            RabbitMqUtil.DEFAULT_HOST, RabbitMqUtil.DEFAULT_PORT, "/", credentials
        )
        return pika.BlockingConnection(parameters)

    @staticmethod
    def declare_exchange(channel, exchange=None, exchange_type=None):
        exchange = exchange or RabbitMqUtil.DEFAULT_EXCHANGE
        exchange_type = exchange_type or RabbitMqUtil.DEFAULT_EXCHANGE_TYPE
        channel.exchange_declare(
            exchange=exchange,
            exchange_type=exchange_type,
            durable=True,
            auto_delete=False,
        )

    @staticmethod
    def publish_message(message: dict, exchange=None, routing_key=""):
        connection = RabbitMqUtil.get_connection()
        channel = connection.channel()

        RabbitMqUtil.declare_exchange(channel, exchange=exchange)

        channel.basic_publish(
            exchange=exchange or RabbitMqUtil.DEFAULT_EXCHANGE,
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type="application/json",
            ),
        )

        connection.close()


class SerializerUtil:
    @staticmethod
    def get_error_messages(serializer_errors):
        """
        Retrieves error messages from a serializer's error dictionary or list.

        Args:
            serializer_errors (dict or list): A dictionary or list containing error messages for fields.

        Returns:
            str: A formatted string of error messages, each indicating
                 the field and its corresponding errors, separated by
                 semicolons.
        """

        if isinstance(serializer_errors, list):
            return "; ".join(str(error) for error in serializer_errors)

        error_messages = []

        for field, errors in serializer_errors.items():
            if isinstance(errors, list):
                clean_errors = []

                for error in errors:
                    if isinstance(error, dict):
                        clean_errors.append(SerializerUtil.get_error_messages(error))
                    else:
                        clean_errors.append(str(error))

                error_str = ", ".join(clean_errors)
            else:
                error_str = str(errors)

            error_messages.append(f"{field}: {error_str}")

        return "; ".join(error_messages)
