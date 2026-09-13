#!/bin/sh

echo "Running database migrations..."

flask --app backend.app db upgrade

echo "Starting Flask application..."

python -m backend.app