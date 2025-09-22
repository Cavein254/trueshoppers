#!/bin/sh

set -e

cd /app

echo "Starting entrypoint script..."

echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=core.settings.dev

echo "Applying database migrations..."
python manage.py migrate

echo "exiting entrypoint..."
exec "$@"
