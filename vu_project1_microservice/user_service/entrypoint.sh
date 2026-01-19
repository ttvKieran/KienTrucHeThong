#!/bin/bash
set -e

echo "Waiting for database to be ready..."
sleep 2

echo "Starting server without auto-migrate..."
exec python manage.py runserver 0.0.0.0:8001
