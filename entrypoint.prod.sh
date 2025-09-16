#!/bin/sh

set -e

echo "Starting entrypoint script..."

echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=core.settings.prod

echo "Applying database migrations..."
python manage.py migrate --settings=core.settings.prod

echo "exiting entrypoint..."
exec "$@"
