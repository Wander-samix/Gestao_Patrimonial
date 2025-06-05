#!/usr/bin/env bash
set -e

# 1) Esperar o banco de dados ficar disponível (útil para Docker Compose):
if [ -n "$DB_HOST" ]; then
  echo "Aguardando o banco de dados em $DB_HOST:$DB_PORT..."
  # netcat verifica a porta até ficar ok
  while ! nc -z $DB_HOST $DB_PORT; do
    sleep 1
  done
fi

# 2) Executar migrações (seminput evita prompt)
echo "Executando migrações..."
python manage.py migrate --noinput

# 3) Coletar arquivos estáticos (sem input)
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear

# 4) Se DEBUG=False (produção), rodar Gunicorn; caso contrário, runserver:
if [ "$DEBUG" = "False" ]; then
  echo "Iniciando Gunicorn em produção..."
  # Ajuste --workers conforme CPU/memória; 'gestao_patrimonial.wsgi:application' é o módulo WSGI
  exec gunicorn gestao_patrimonial.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level=info
else
  echo "DEBUG=True, iniciando servidor de desenvolvimento do Django..."
  exec python manage.py runserver 0.0.0.0:8000
fi
