#!/usr/bin/env bash

# I use arch u use arch to

sudo pacman -Syu
sudo pacman -S postgresql
sudo -iu postgres initdb --locale $LANG -E UTF8 -D '/var/lib/postgres/data'
sudo systemctl start postgresql.service

sudo -iu postgres psql <<EOF

CREATE DATABASE web;

CREATE USER lwall WITH ENCRYPTED PASSWORD 'yourpassword';

GRANT ALL PRIVILEGES ON DATABASE web TO lwall;

\c web

GRANT ALL PRIVILEGES ON SCHEMA public TO lwall;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO lwall;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO lwall;

\dn+ public

SELECT * FROM users;
SELECT * FROM baskets;

EOF

# Create and activate a virtual environment
python3 -m venv env
source env/bin/activate

# Install Django and other necessary packages
pip install django djangorestframework djangorestframework-simplejwt channels channels-redis psycopg2-binary

# Create a new Django project
django-admin startproject trello_backend
cd trello_backend

# Create a new app within the project
python manage.py startapp api


# after setup code
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver