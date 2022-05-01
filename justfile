alias t := test

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

#### production ###############################################################

prod-build:
  docker build -f src/Dockerfile.prod -t \
    registry.heroku.com/polar-wave-90516/web ./src

prod-run:
  docker run --name app -e PORT=8765 -e DATABASE_URL=sqlite://sqlite.db \
    -p 5003:8765 registry.heroku.com/polar-wave-90516/web:latest

prod-push:
  docker push registry.heroku.com/polar-wave-90516/web:latest

prod-release:
  heroku container:release web --app polar-wave-90516

prod-migrate:
  heroku run aerich upgrade --app polar-wave-90516
