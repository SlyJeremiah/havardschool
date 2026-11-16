#!/bin/bash
# Vercel static build: install deps, collect static files and apply migrations.
set -e

PY=$(command -v python3.12 || command -v python3)
echo "Using $($PY --version)"

$PY -m pip install -r requirements.txt --quiet --disable-pip-version-check \
  || $PY -m pip install -r requirements.txt --quiet --break-system-packages

$PY manage.py collectstatic --noinput --clear

# Apply database migrations on each deploy (needs DATABASE_URL in the build env)
if [ -n "$DATABASE_URL" ]; then
  $PY manage.py migrate --noinput
  # Loads starter content on the very first deploy only
  $PY manage.py seed_site --once
  # Creates the first admin from DJANGO_SUPERUSER_* variables (skips if unset or already exists)
  $PY manage.py ensure_superuser
fi
