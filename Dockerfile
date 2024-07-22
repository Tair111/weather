# Используем базовый образ Python с поддержкой Flask
FROM python:3.8.0

# Установка зависимостей проекта
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

# Копирование кода проекта в контейнер
COPY . /app

# Определение переменных окружения
ENV FLASK_APP=app.py

# Открытие порта для веб-приложения
EXPOSE 5000

# Команда для запуска приложения
CMD ["flask", "run", "--host=0.0.0.0"]