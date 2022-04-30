set dotenv-load := true
set positional-arguments := true

down:
  docker-compose down

logs-web:
  docker-compose logs web

up:
  docker-compose up -d --build

@watch-test *args='.':
  watchexec -w=app/ -- just test "$@"
