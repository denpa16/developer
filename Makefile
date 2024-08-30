THIS_FILE := $(lastword $(MAKEFILE_LIST))

COMPOSE_FILES := -f docker-compose.yml -f docker-compose.override.yml


alembicinit:
	docker-compose $(COMPOSE_FILES) exec backend poetry run alembic init "$(c)"
# e.g.
# make alembicinit c=./app/data/migrations

makemigrations:
	docker-compose $(COMPOSE_FILES) exec backend poetry run alembic revision --autogenerate -m "$(c)"

migrate:
	docker-compose $(COMPOSE_FILES) exec backend poetry run alembic upgrade head

downgrate:
	docker-compose $(COMPOSE_FILES) exec backend poetry run alembic downgrade "$(c)"

tests:
	docker-compose $(COMPOSE_FILES) exec backend poetry run pytest $(c)

lock:
	docker-compose $(COMPOSE_FILES) exec backend poetry lock

linters:
	docker-compose $(COMPOSE_FILES) exec backend poetry run ruff check . --fix

format:
	docker-compose $(COMPOSE_FILES) exec backend poetry run ruff format .

lint-check:
	docker-compose $(COMPOSE_FILES) exec backend poetry run ruff check .
