#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line to match your project's setup
pip install -r requirements.txt

# Run migrations if needed (uncomment the next line)
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input