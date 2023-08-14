#!/bin/sh

echo "Adding migrations to database..."
python manage.py makemigrations
python manage.py migrate

echo "Rebuilding search index..."
python manage.py search_index --rebuild -f

echo "Starting the server..."
if [[ $ENVIRONMENT == "PRODUCTION" ]]; then
    gunicorn config.wsgi --bind 0.0.0.0:8000
else
    python manage.py runserver 0.0.0.0:8000
fi
