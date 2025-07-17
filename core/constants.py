from django.utils.translation import gettext_lazy as _


class CacheConstant:
    """
    CacheConstant holds the cache configurations
    """

    TIMEOUT = 86400
    TIMEOUT_SHORT = 3600
    TYPE_MODEL = "t_model"
    TYPE_ENDPOINT = "t_endpoint"
    SEPERATOR = "--"
    SOURCE_VIEW_MODEL_VIEW_SET = "s_view_model_viewset"
    SOURCE_VIEW_API_VIEW = "s_view_model_api_view"
    SOURCE_SIGNAL = "s_signal"


class ConfigConstant:
    """
    ConfigConstant holds the configuration keys used in the application.
    """

    USER_SERVICE_NAME = "user-service"
    USER_SERVICE_API = f"http://{USER_SERVICE_NAME}:8000"

    RABBITMQ_HOST = "rabbitmq"
    RABBITMQ_PORT = 5672
    RABBITMQ_USER = "rabbit_user"
    RABBITMQ_PASS = "rabbit_pass"


class ErrorConstant:
    BAD_REQUEST = 400
    UNAUTHORIZED_STATUS_CODE = 401
    NOT_FOUND_STATUS_CODE = 404
    INTERNAL_SERVER_ERROR = 500


class GroupConstant:
    """
    GroupConstant holds the names of user groups in the application.
    """

    ADMIN = "admin"
    DEVELOPER = "developer"

    TECHNICAL_ROLES = [DEVELOPER]

    ALL_GROUPS = list({ADMIN, *TECHNICAL_ROLES})


class LanguageConstant:
    """
    LanguageConstant holds the active language configuration for the application.
    """

    CURRENT_LANGUAGE = "tr"

    SUPPORTED_LANGUAGES = [
        ("tr", "Türkçe"),
        ("en", "English"),
    ]

    PARLER_LANGUAGES = {
        None: tuple({"code": l[0]} for l in SUPPORTED_LANGUAGES),
        "default": {
            "fallbacks": [CURRENT_LANGUAGE],
            "hide_untranslated": False,
        },
    }


class MessageConstant:
    UNAUTHORIZED = _("Invalid credentials")
    NOT_EXIST_PERMISSION = _("You do not have permission to perform this action.")
    NOT_MATCH_ANY_RECORD = _("No matching records found")

    SUCCESS_CREATE = _("Successfully created")
    SUCCESS_DELETE = _("Successfully deleted")
    SUCCESS_UPDATE = _("Successfully updated")
    SUCCESS_LIST = _("Successfully listed")
    SUCCESS_RETRIEVE = _("Successfully retrieved")

    ERROR_SERVICE_REQUEST = _("Service request failed")
