#!/bin/bash

# Скрипт для сборки и деплоя в Docker Hub
# Использование: ./deploy.sh [version]

set -e

# Конфигурация
DOCKER_USERNAME="dedzyuka"
IMAGE_NAME="chatbot"
VERSION=${1:-latest}

echo "🚀 Начинаем деплой $DOCKER_USERNAME/$IMAGE_NAME:$VERSION"

# Проверка авторизации в Docker Hub
echo "📋 Проверка авторизации в Docker Hub..."
if ! docker info | grep -q "Username: $DOCKER_USERNAME"; then
    echo "❌ Необходимо авторизоваться в Docker Hub"
    echo "Выполните: docker login"
    exit 1
fi

# Сборка образа
echo "🔨 Сборка Docker образа..."
docker build -t $DOCKER_USERNAME/$IMAGE_NAME:$VERSION .
docker build -t $DOCKER_USERNAME/$IMAGE_NAME:latest .

# Тест образа
echo "🧪 Тестирование образа..."
docker run --rm -d --name test-container $DOCKER_USERNAME/$IMAGE_NAME:$VERSION sleep 10
sleep 5
docker stop test-container || true

# Загрузка в Docker Hub
echo "📤 Загрузка образа в Docker Hub..."
docker push $DOCKER_USERNAME/$IMAGE_NAME:$VERSION
docker push $DOCKER_USERNAME/$IMAGE_NAME:latest

echo "✅ Успешно загружено в Docker Hub!"
echo "📦 Образ доступен по адресу: docker.io/$DOCKER_USERNAME/$IMAGE_NAME:$VERSION"

# Показать команды для запуска
echo ""
echo "🎯 Команды для запуска:"
echo "docker run -d --name chatbot \\"
echo "  -e BOT_TOKEN=your_token \\"
echo "  -e OPENAI_API_KEY=your_key \\"
echo "  -e GEMINI_EMBEDD=your_key \\"
echo "  -e DB_URI=postgresql://user:pass@host:5432/db \\"
echo "  $DOCKER_USERNAME/$IMAGE_NAME:$VERSION"
echo ""
echo "Или используйте docker-compose:"
echo "docker-compose pull && docker-compose up -d"
