up:
	docker-compose up --build -d

down:
	docker-compose down --volumes --remove-orphans

rebuild:
	docker-compose down --volumes --remove-orphans
	docker-compose build --no-cache
	docker-compose up -d
