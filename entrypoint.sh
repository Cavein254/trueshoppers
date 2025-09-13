#!/bin/sh

set -e

echo "Starting entrypoint script..."

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Applying database migrations..."
python manage.py migrate

echo "exiting entrypoint..."
exec "$@"