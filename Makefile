.PHONY: help build run stop test admin local_confmap prod_confmap

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
	@echo "  local_confmap - Make Kubernetes config maps for local stage"
	@echo "  prod_confmap - Make Kubernetes config maps for production stage"

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

local_confmap:
	kubectl create configmap academy-master-env --from-env-file=./backend/.env.local && kubectl create configmap academy-master-env-file --from-file=.env=./backend/.env.local &&  kubectl create configmap postgres-initdb --from-file=./backend/docker/commands/pg-entrypoint.sh && kubectl create configmap prometheus-config --from-file=./prometheus/config.yaml

prod_confmap:
	kubectl create configmap academy-master-env --from-env-file=./backend/.env.prod && kubectl create configmap academy-master-env-file --from-file=.env=./backend/.env.prod &&  kubectl create configmap postgres-initdb --from-file=./backend/docker/commands/pg-entrypoint.sh && kubectl create configmap prometheus-config --from-file=./prometheus/config.yaml

load_mock_data:
	docker exec academy-master-backend python manage.py loaddata sample-db.json