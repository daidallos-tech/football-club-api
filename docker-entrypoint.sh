#!/bin/sh

set -e

echo "Running database migrations..."

uv run alembic upgrade head

echo "Starting FastAPI..."

export PYTHONPATH=$PYTHONPATH:/src/football_club_api/src

exec uv run uvicorn main:app --app-dir src/football_club_api --host 0.0.0.0 --port 8000