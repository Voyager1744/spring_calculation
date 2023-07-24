# Используем базовый образ с Python 3.11
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл requirements.txt в контейнер
COPY requirements.txt .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все содержимое проекта в контейнер
COPY . .

# Добавляем корректный путь к корневому каталогу проекта в PYTHONPATH
ENV PYTHONPATH="/app"

# Запускаем приложение при старте контейнера
CMD ["python", "backend/bot/telegram_bot.py"]