#!/usr/bin/env bash
set -e

if [ -n "$DB_HOST" ]; then
  echo "Aguardando o banco de dados em $DB_HOST:$DB_PORT..."
  while ! nc -z $DB_HOST $DB_PORT; do
    sleep 1
  done
fi

echo "Executando migrações..."
python manage.py migrate --noinput

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear

if [ "$DEBUG" = "False" ]; then
  echo "Iniciando Gunicorn em produção..."
  exec gunicorn gestao_patrimonial.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level=info
else
  echo "DEBUG=True, iniciando servidor de desenvolvimento do Django..."
  exec python manage.py runserver 0.0.0.0:8000
fi
