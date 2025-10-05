#!/bin/bash

# Автоматическая установка AI Telegram Bot
# Использование: ./install.sh

set -e

echo "🤖 AI Telegram Bot - Автоматическая установка"
echo "=============================================="

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен!"
    echo "📥 Установите Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

echo "✅ Docker найден"

# Проверка docker-compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose не найден!"
    echo "📥 Установите docker-compose"
    exit 1
fi

echo "✅ docker-compose найден"

# Создание .env файла
if [ ! -f .env ]; then
    echo "📝 Создание файла .env..."
    cp env.example .env
    echo "⚠️  ВАЖНО: Отредактируйте файл .env с вашими API ключами!"
    echo "   nano .env"
    echo ""
    echo "Обязательные ключи:"
    echo "   - BOT_TOKEN (получить у @BotFather)"
    echo "   - OPENAI_API_KEY (получить на platform.openai.com)"
    echo "   - GEMINI_EMBEDD (получить на aistudio.google.com)"
    echo ""
    read -p "Нажмите Enter когда заполните .env файл..."
fi

# Проверка .env файла
if grep -q "your_.*_here" .env; then
    echo "❌ Файл .env не настроен!"
    echo "📝 Отредактируйте .env файл с вашими API ключами"
    exit 1
fi

echo "✅ Файл .env настроен"

# Скачивание образа
echo "📥 Скачивание образа dedzyuka/chatbot:latest..."
docker pull dedzyuka/chatbot:latest

# Запуск сервисов
echo "🚀 Запуск сервисов..."
docker-compose up -d

# Ожидание запуска
echo "⏳ Ожидание запуска сервисов..."
sleep 10

# Проверка статуса
echo "📊 Проверка статуса..."
if docker ps | grep -q chatbot && docker ps | grep -q postgres; then
    echo "✅ Все сервисы запущены успешно!"
    echo ""
    echo "🎉 Бот готов к работе!"
    echo ""
    echo "📋 Полезные команды:"
    echo "   docker logs -f chatbot    # Просмотр логов"
    echo "   docker-compose stop       # Остановка"
    echo "   docker-compose restart    # Перезапуск"
    echo ""
    echo "🌐 Веб-интерфейсы:"
    echo "   pgAdmin: http://localhost:8080 (admin@example.com / admin)"
    echo ""
    echo "📱 Найдите своего бота в Telegram и отправьте /start"
else
    echo "❌ Ошибка запуска сервисов"
    echo "📋 Проверьте логи:"
    echo "   docker logs chatbot"
    echo "   docker logs postgres-bot"
    exit 1
fi
