#!/bin/sh
set -e

echo "xx Starting entrypoint script..."

cd /app

echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=core.settings.prod

echo "Applying database migrations..."
python manage.py migrate --settings=core.settings.prod

echo "Entrypoint finished, starting app..."

exec "$@"
