#!/bin/sh

echo "Running celery worker..."
celery -A config worker --loglevel=CRITICAL