.PHONY: up down rebuild lint lint-fix format test

up:
	docker-compose up --build -d

down:
	docker-compose down --volumes --remove-orphans

rebuild:
	docker-compose down --volumes --remove-orphans
	docker-compose build --no-cache
	docker-compose up -d

lint:
	docker-compose run --rm backend ruff check /app

lint-fix:
	docker-compose run --rm backend ruff check --fix /app

format:
	docker-compose run --rm backend black /app

shell:
	docker-compose run --rm backend bash

test:
	docker-compose run --rm backend pytest --cov=. --cov-report=term tests/

coverage:
	docker-compose run --rm backend pytest --cov=. --cov-report=html tests/

clean:
	rm -rf backend/htmlcov
	rm -rf backend/.pytest_cache
	rm -rf backend/.ruff_cache