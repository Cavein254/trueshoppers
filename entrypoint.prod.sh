#!/bin/sh
set -e

echo "Starting entrypoint script..."

cd /app

echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=core.settings.prod

echo "Applying database migrations..."
python manage.py migrate --settings=core.settings.prod

echo "Entrypoint finished, starting app..."

# Run Gunicorn
exec gunicorn core.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --log-level info
