set dotenv-load := true
set positional-arguments := true

build:
  docker-compose build

logs-web:
  docker-compose logs web

up:
  docker-compose up -d

@watch-test *args='.':
  watchexec -w=app/ -- just test "$@"
