#!/bin/sh

echo "[INFO]: allpy data base migrations"
python manage.py migrate

echo "[INFO]: transfer data from SQLite to PostgreSQL"
python load_data.py

echo "[INFO]: run server"
uwsgi --ini uwsgi.ini
