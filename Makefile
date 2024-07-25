.PHONY: help build run stop test admin

help:
	@echo "Available targets:"
	@echo "  help    - Show this help message."
	@echo "  build   - Build the docker image."
	@echo "  run     - Run the docker container."
	@echo "  deploy  - Deploy the docker container."
	@echo "  stop    - Stop the docker container."
	@echo "  test    - Run the tests."
	@echo "  migrations - Create migrations."
	@echo "  migrate - Migrate"


build:
	docker compose build

run:
ifeq ($(DETACHED),true)
	docker compose up -d
else
	docker compose up
endif

deploy:
	docker compose -f docker-compose.prod.yml up -d

stop:
	docker compose down

test:
	docker exec academy-master-backend pytest

migrations:
	docker exec academy-master-backend python manage.py makemigrations

migrate:
	docker exec academy-master-backend python manage.py migrate
