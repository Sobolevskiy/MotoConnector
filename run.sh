#!/usr/bin/env bash

set -ex
function create_superuser() {
  DJANGO_SUPERUSER_PASSWORD=root python manage.py createsuperuser \
      --noinput \
      --username root \
      --email "mi8sobolev@mail.ru"
}

python3 manage.py migrate
create_superuser
python3 manage.py collectstatic --noinput
python3 manage.py runserver