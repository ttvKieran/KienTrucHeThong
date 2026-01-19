#!/bin/bash
set -e

echo "Waiting for database to be ready..."
sleep 2

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8002
