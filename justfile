alias t := test

set dotenv-load := true
set positional-arguments := true

#### local ####################################################################

db-migrate:
  docker compose exec web aerich migrate

db-upgrade:
  docker compose exec web aerich upgrade

down:
  docker compose down

logs-web:
  docker compose logs web

psql:
  docker compose exec web-db psql -U postgres

@test *args='.':
  docker compose exec web python -m pytest "$@"

up:
  docker compose up -d --build

#### heroku ###################################################################

heroku-build:
  docker build -f src/Dockerfile.prod \
    -t registry.heroku.com/sheltered-falls-06080/web ./src

heroku-run:
  docker run --name app -e PORT=8765 -e DATABASE_URL=sqlite://sqlite.db \
    -p 5003:8765 registry.heroku.com/sheltered-falls-06080/web:latest

heroku-push:
  docker push registry.heroku.com/sheltered-falls-06080/web:latest

heroku-release:
  heroku container:release web --app sheltered-falls-06080

heroku-migrate:
  heroku run aerich upgrade --app sheltered-falls-06080

#### production ###############################################################

prod-build:
  docker build -f src/Dockerfile.prod -t web ./src

prod-build-github:
  docker build -f src/Dockerfile.prod \
    -t docker.pkg.github.com/dycw/tutorial-test-driven-development-with-fastapi-and-docker/summarizer:latest \
    ./src

prod-rm:
  docker rm app -f

prod-run:
  docker run --name app -e PORT=8765 -e DATABASE_URL=sqlite://sqlite.db \
    -p 5003:8765 web:latest

prod-push-github:
  docker push docker.pkg.github.com/dycw/tutorial-test-driven-development-with-fastapi-and-docker/summarizer:latest
