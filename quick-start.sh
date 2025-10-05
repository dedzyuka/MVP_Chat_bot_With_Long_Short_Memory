#!/bin/bash

# Быстрый запуск бота с готовым образом из Docker Hub
# Использование: ./quick-start.sh

set -e

echo "🤖 Быстрый запуск AI Telegram Bot"
echo "=================================="

# Проверка наличия .env файла
if [ ! -f .env ]; then
    echo "❌ Файл .env не найден!"
    echo "📝 Создайте файл .env с необходимыми переменными:"
    echo ""
    echo "BOT_TOKEN=your_telegram_bot_token"
    echo "OPENAI_API_KEY=your_openai_api_key"
    echo "GEMINI_EMBEDD=your_google_ai_api_key"
    echo "DB_URI=postgresql://user:password@localhost:5432/database"
    echo ""
    echo "Или скопируйте пример:"
    echo "cp .env.example .env"
    echo "nano .env"
    exit 1
fi

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен!"
    echo "Установите Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Скачивание последней версии образа
echo "📥 Скачивание образа dedzyuka/chatbot:latest..."
docker pull dedzyuka/chatbot:latest

# Остановка и удаление предыдущего контейнера
echo "🛑 Остановка предыдущих контейнеров..."
docker stop telegram-bot-app 2>/dev/null || true
docker rm telegram-bot-app 2>/dev/null || true

# Запуск бота
echo "🚀 Запуск бота..."
docker run -d \
    --name telegram-bot-app \
    --env-file .env \
    --restart unless-stopped \
    dedzyuka/chatbot:latest

# Проверка запуска
echo "⏳ Ожидание запуска..."
sleep 3

if docker ps | grep -q telegram-bot-app; then
    echo "✅ Бот успешно запущен!"
    echo ""
    echo "📊 Полезные команды:"
    echo "  docker logs -f telegram-bot-app    # Просмотр логов"
    echo "  docker stop telegram-bot-app       # Остановка бота"
    echo "  docker restart telegram-bot-app    # Перезапуск бота"
    echo "  docker ps                          # Статус контейнеров"
    echo ""
    echo "🎯 Бот готов к работе!"
else
    echo "❌ Ошибка запуска бота"
    echo "📋 Проверьте логи:"
    echo "docker logs telegram-bot-app"
    exit 1
fi
