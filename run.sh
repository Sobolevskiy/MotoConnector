#!/bin/bash

set -ex

function wait_for_dbs() {
  ./wait-for-it.sh -s "$DB_HOST:$DB_PORT" --timeout=180
}

[ -f /venv/bin/activate ] && . /venv/bin/activate

if [[ "$1" == "runserver" ]]; then
  wait_for_dbs
  python3 manage.py migrate --noinput
  python3 manage.py super_user_creation --username root --password root --email mi8sobolev@mail.ru --preserve  --noinput
  python3 manage.py collectstatic --noinput
  python3 manage.py runserver 0.0.0.0:8000
else
  exec "$@"
fi