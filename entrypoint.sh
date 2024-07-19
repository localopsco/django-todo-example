#!/bin/bash
set -e

# Apply migrations
python manage.py migrate

# Start the Django application
exec "$@"
