FROM python:3.11-slim

# Настройки Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Системные зависимости
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn  # Обязательно для продакшена

COPY . .

# Сбор статики (нужно для корректного отображения стилей)
# Перед этим убедитесь, что в settings.py настроен STATIC_ROOT
RUN python manage.py collectstatic --noinput

# Railway сам подставит нужный PORT через переменную окружения
CMD gunicorn config.wsgi:application --bind 0.0.0.0:$PORT