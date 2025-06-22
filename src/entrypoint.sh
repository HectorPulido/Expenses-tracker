#!/bin/sh
python manage.py migrate
python manage.py collectstatic --no-input

if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi
$@

# For testing
# python manage.py runserver 0.0.0.0:8000

gunicorn expenses_tracker.wsgi:application --bind 0.0.0.0:8000  --timeout 240 --workers 3 --log-level=debug

