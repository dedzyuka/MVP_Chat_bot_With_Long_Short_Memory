# Makefile для AI Telegram Bot

.PHONY: help build push deploy run stop logs clean test

# Переменные
DOCKER_USERNAME = dedzyuka
IMAGE_NAME = chatbot
VERSION = latest

help: ## Показать справку
	@echo "🤖 AI Telegram Bot - Команды управления"
	@echo "========================================"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Собрать Docker образ
	@echo "🔨 Сборка образа $(DOCKER_USERNAME)/$(IMAGE_NAME):$(VERSION)"
	docker build -t $(DOCKER_USERNAME)/$(IMAGE_NAME):$(VERSION) .
	docker build -t $(DOCKER_USERNAME)/$(IMAGE_NAME):latest .

push: ## Загрузить образ в Docker Hub
	@echo "📤 Загрузка в Docker Hub..."
	docker push $(DOCKER_USERNAME)/$(IMAGE_NAME):$(VERSION)
	docker push $(DOCKER_USERNAME)/$(IMAGE_NAME):latest

deploy: build push ## Собрать и загрузить образ
	@echo "✅ Деплой завершен!"

run: ## Запустить бота локально
	@echo "🚀 Запуск бота..."
	docker-compose up -d

stop: ## Остановить бота
	@echo "🛑 Остановка бота..."
	docker-compose down

logs: ## Показать логи бота
	@echo "📋 Логи бота:"
	docker-compose logs -f bot

quick: ## Быстрый запуск с готовым образом
	@echo "⚡ Быстрый запуск..."
	./quick-start.sh

clean: ## Очистить Docker кэш и неиспользуемые образы
	@echo "🧹 Очистка Docker..."
	docker system prune -f
	docker image prune -f

test: ## Тестирование образа
	@echo "🧪 Тестирование образа..."
	docker run --rm -d --name test-bot $(DOCKER_USERNAME)/$(IMAGE_NAME):$(VERSION) sleep 10
	sleep 5
	docker stop test-bot

install: ## Установить зависимости локально
	@echo "📦 Установка зависимостей..."
	pip install -r requirements.txt

dev: ## Запуск в режиме разработки
	@echo "🔧 Режим разработки..."
	python main.py

status: ## Показать статус контейнеров
	@echo "📊 Статус контейнеров:"
	docker ps -a | grep -E "(telegram-bot|postgres)"

pull: ## Скачать последнюю версию образа
	@echo "📥 Скачивание образа..."
	docker pull $(DOCKER_USERNAME)/$(IMAGE_NAME):latest
