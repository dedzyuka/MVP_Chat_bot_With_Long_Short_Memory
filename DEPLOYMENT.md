# 🚀 Инструкции по деплою

## Docker Hub Setup

### 1. Авторизация в Docker Hub

```bash
# Локальная авторизация
docker login

# Введите username: dedzyuka
# Введите password: [ваш пароль Docker Hub]
```

### 2. Сборка и загрузка образа

```bash
# Автоматический деплой
./deploy.sh

# Или ручная сборка
docker build -t dedzyuka/chatbot:latest .
docker push dedzyuka/chatbot:latest
```

### 3. Проверка загрузки

```bash
# Проверка доступности образа
docker pull dedzyuka/chatbot:latest

# Тестовый запуск
docker run --rm dedzyuka/chatbot:latest --help
```

## GitHub Actions Setup

### 1. Настройка Secrets в GitHub

В репозитории перейдите в Settings → Secrets and variables → Actions и добавьте:

- `DOCKER_USERNAME`: `dedzyuka`
- `DOCKER_PASSWORD`: [ваш пароль Docker Hub]

### 2. Автоматическая сборка

GitHub Actions автоматически:
- Собирает образ при push в main/master
- Создает теги при создании релизов
- Загружает в Docker Hub с соответствующими тегами

### 3. Тегирование релизов

```bash
# Создание релиза
git tag v1.0.0
git push origin v1.0.0

# GitHub Actions автоматически создаст образ с тегом v1.0.0
```

## Локальный деплой

### Быстрый запуск

```bash
# Скачать и запустить готовый образ
docker run -d --name chatbot \
  -e BOT_TOKEN=your_token \
  -e OPENAI_API_KEY=your_key \
  -e GEMINI_EMBEDD=your_key \
  -e DB_URI=postgresql://user:pass@host:5432/db \
  dedzyuka/chatbot:latest
```

### С Docker Compose

```bash
# Скачать последнюю версию
docker-compose pull

# Запустить все сервисы
docker-compose up -d
```

## Production Deployment

### 1. Настройка переменных окружения

Создайте файл `.env.production`:

```env
BOT_TOKEN=your_production_token
OPENAI_API_KEY=your_production_key
GEMINI_EMBEDD=your_production_key
DB_URI=postgresql://prod_user:secure_password@prod_host:5432/prod_db
MAX_MESSAGES=50
MAX_TOKENS=8000
```

### 2. Запуск в production

```bash
# С production конфигурацией
docker run -d --name chatbot-prod \
  --env-file .env.production \
  --restart unless-stopped \
  dedzyuka/chatbot:latest
```

### 3. Мониторинг

```bash
# Просмотр логов
docker logs -f chatbot-prod

# Проверка статуса
docker ps | grep chatbot

# Перезапуск при обновлении
docker pull dedzyuka/chatbot:latest
docker stop chatbot-prod
docker rm chatbot-prod
docker run -d --name chatbot-prod \
  --env-file .env.production \
  --restart unless-stopped \
  dedzyuka/chatbot:latest
```

## Troubleshooting

### Проблемы с авторизацией

```bash
# Проверка авторизации
docker system info | grep Username

# Повторная авторизация
docker logout
docker login
```

### Проблемы со сборкой

```bash
# Очистка кэша Docker
docker system prune -a

# Пересборка без кэша
docker build --no-cache -t dedzyuka/chatbot:latest .
```

### Проблемы с загрузкой

```bash
# Проверка размера образа
docker images dedzyuka/chatbot

# Сжатие образа
docker build --squash -t dedzyuka/chatbot:latest .
```
