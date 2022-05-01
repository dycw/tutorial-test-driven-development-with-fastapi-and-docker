set dotenv-load := true
set positional-arguments := true

down:
  docker-compose down

logs-web:
  docker-compose logs web

@test *args='.':
  docker-compose exec web python -m pytest "$@"

up:
  docker-compose up -d --build
