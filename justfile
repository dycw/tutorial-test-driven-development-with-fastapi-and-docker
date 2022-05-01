set dotenv-load := true
set positional-arguments := true

down:
  docker-compose down

logs-web:
  docker-compose logs web

migrate:
  docker-compose exec web aerich migrate

psql:
  docker-compose exec web-db psql -U postgres

@test *args='.':
  docker-compose exec web python -m pytest "$@"

up:
  docker-compose up -d --build
