#!/bin/sh
poetry run wait-for
poetry run alembic upgrade head
exec "$@"