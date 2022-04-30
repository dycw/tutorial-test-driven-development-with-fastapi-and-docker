set dotenv-load := true
set positional-arguments := true

build:
  docker-compose build

@run *args='':
  docker-compose run app "$@"

@manage *args='':
  just run python manage.py "$@"

@test *args='.':
  just manage test "$@"

up:
  docker-compose up -d

@watch-test *args='.':
  watchexec -w=app/ -- just test "$@"
