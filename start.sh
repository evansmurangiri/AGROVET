#!/bin/bash
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn djecommerce.wsgi:application