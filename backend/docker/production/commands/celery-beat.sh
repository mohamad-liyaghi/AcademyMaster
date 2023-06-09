#!/bin/sh

echo "Running celery beat worker..."
celery -A config beat --loglevel=CRITICAL