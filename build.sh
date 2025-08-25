#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies including gunicorn
pip install -r requirements.txt
pip install gunicorn

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input