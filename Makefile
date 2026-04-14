.PHONY: dev down clean status

# Changed 'docker-compose' to 'docker compose'
dev:
	docker compose up --build -d

status:
	docker compose ps

down:
	docker compose down

clean:
	docker compose down -v
	docker system prune -f
