.PHONY: dev down clean status logs test

# Changed 'docker-compose' to 'docker compose'
dev:
	docker compose up -d

build:
	docker compose up --build -d

status:
	docker compose ps

down:
	docker compose down

clean:
	docker compose down -v
	docker system prune -f

logs:
	docker compose logs -f

test:
	docker compose exec backend uv run pytest
