.PHONY: up down dagster test logs clean

up:
	docker compose up -d postgres adminer
	@echo "Postgres et Adminer démarrés. Adminer : http://localhost:8080"

down:
	docker compose down

dagster:
	dagster dev -m src.assets

dashboard:
	docker compose up -d --build dashboard
	@echo "Dashboard : http://localhost:8501"

test:
	pytest tests/ -v

logs:
	docker compose logs -f

clean:
	docker compose down -v