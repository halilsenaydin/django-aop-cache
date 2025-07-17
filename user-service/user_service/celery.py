"""
Celery configuration file for the 'user_service' Django application.

This file initializes the Celery application, configures it using Django settings,
and enables automatic discovery of tasks across all registered Django apps.

Usage:
- Celery will use the 'user_service.settings' module for configuration.
- All tasks defined in 'tasks.py' files within installed apps will be discovered automatically.

To start the Celery worker:
    celery -A user_service worker --loglevel=info

Make sure that the Django settings file includes appropriate CELERY_* configurations.

"""

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "user_service.settings")

app = Celery("user_service")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
