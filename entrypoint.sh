#!/bin/sh

echo "INSIDE ENTRYPOINT"
cd cms
ls
python manage.py migrate
python manage.py runserver
echo "EXITING ENTRYPOINT"