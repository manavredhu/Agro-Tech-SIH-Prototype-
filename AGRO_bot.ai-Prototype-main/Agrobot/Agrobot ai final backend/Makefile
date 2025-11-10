
.PHONY: up down logs seed test

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f web

seed:
	docker compose exec web python app/seed.py
