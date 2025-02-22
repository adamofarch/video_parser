#!/bin/sh

python manage.py migrate
python manage.py collectstatic --noinput --clear >/dev/null
celery -A video_parser worker -E -l INFO &
python manage.py runserver 0.0.0.0:8000
