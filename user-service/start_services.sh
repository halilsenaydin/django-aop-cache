#!/bin/bash

echo "Starting Celery worker..."
celery -A user_service worker --loglevel=info &

wait
