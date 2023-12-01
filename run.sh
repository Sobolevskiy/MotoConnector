#!/bin/bash

set -ex
function create_superuser() {
  DJANGO_SUPERUSER_PASSWORD=root python manage.py createsuperuser \
      --noinput \
      --username root \
      --email "mi8sobolev@mail.ru"
}

[ -f /venv/bin/activate ] && . /venv/bin/activate

if [[ "$1" == "runserver" ]]; then
python3 manage.py migrate --noinput
create_superuser
python3 manage.py collectstatic --noinput
python3 manage.py runserver 0.0.0.0:8000
else
  exec "$@"
fi