#!/usr/bin/env bash
# Build script for Vercel deployment
set -e

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Collecting static assets..."
python3 manage.py collectstatic --noinput --clear

echo "Vercel build complete."

