#!/bin/sh

if [[ $ENVIRONMENT == "PRODUCTION" ]]; then
    LOGLEVEL="CRITICAL"
else
    LOGLEVEL="DEBUG"
fi

echo "Running celery worker..."
celery -A config worker --loglevel=$LOGLEVEL
