#!/bin/bash

if [[ -z $APP_NAME ]]; then
	echo "Variable APP_NAME not set - Please set this using the -e flag"
    exit 1
else
    cd /app
    yes | python manage.py makemigrations --merge
    yes | python manage.py migrate
	python manage.py collectstatic --noinput
  uwsgi --http :8001 \
   --http-websockets \
   --processes 2 \
   --threads 2 \
   --wsgi-file /app/$APP_NAME/wsgi.py
fi