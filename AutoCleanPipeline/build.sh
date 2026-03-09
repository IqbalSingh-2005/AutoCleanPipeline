#!/usr/bin/env bash
# Render build script
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

cd AutoCleanSet
mkdir -p media
python manage.py collectstatic --no-input
python manage.py migrate
