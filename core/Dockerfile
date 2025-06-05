# Etapa 1: construir a imagem Python e copiar o código
FROM python:3.10-slim

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Para evitar prompts durante instalação de pacotes do sistema
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências de sistema necessárias (geralmente para PostgreSQL, libpq etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
 && rm -rf /var/lib/apt/lists/*

# Copia o arquivo requirements.txt para dentro do container
COPY backend/requirements.txt /app/requirements.txt

# Instala as dependências Python
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Copia todo o código do Django para dentro do container
COPY backend/ /app/

# Executa as migrations e coleta arquivos estáticos durante o build (opcional, mas recomendável)
# Caso prefira fazer durante o startup, retire estes comandos e faça no entrypoint
RUN python manage.py makemigrations --noinput
RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput

# Expõe a porta em que a aplicação Django (por Gunicorn) vai rodar
EXPOSE 8000

# Comando padrão para executar o Gunicorn
CMD ["gunicorn", "meu_projeto.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
