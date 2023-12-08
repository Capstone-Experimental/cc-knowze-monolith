.PHONY: run-prod down-prod run-dev down-dev

run-prod:
	docker-compose -f docker-compose.prod.yml up -d

down-prod:
	docker-compose -f docker-compose.prod.yml down

run-dev:
	docker-compose -f docker-compose.dev.yml up -d

down-dev:
	docker-compose -f docker-compose.dev.yml down
