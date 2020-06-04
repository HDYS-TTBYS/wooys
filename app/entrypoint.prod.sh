#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "migrate"
python manage.py migrate
echo "collectstatic"
python manage.py collectstatic --no-input --clear
echo "gunicorn"
gunicorn config.wsgi:application --bind 0.0.0.0:8000

exec "$@"
