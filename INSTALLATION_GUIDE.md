# 🚀 Полная инструкция по установке AI Telegram Bot

## 📋 Что вы получите

- AI Telegram бот с краткосрочной и долгосрочной памятью
- Готовый к работе Docker образ
- PostgreSQL база данных
- Векторный поиск и эмбеддинги
- Веб-интерфейс для управления БД (pgAdmin)

---

## 🖥️ Требования к системе

- **OS**: Windows 10/11, macOS, или Linux
- **RAM**: Минимум 4GB (рекомендуется 8GB)
- **Disk**: Минимум 2GB свободного места
- **Internet**: Стабильное подключение

---

## 📦 Шаг 1: Установка Docker

### Windows
1. Скачайте [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Запустите установщик и следуйте инструкциям
3. Перезагрузите компьютер
4. Запустите Docker Desktop

### macOS
1. Скачайте [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Перетащите приложение в папку Applications
3. Запустите Docker Desktop

### Linux (Ubuntu/Debian)
```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Добавление пользователя в группу docker
sudo usermod -aG docker $USER

# Перезагрузка для применения изменений
sudo reboot
```

---

## 📥 Шаг 2: Клонирование проекта

### Через Git (рекомендуется)
```bash
# Клонирование репозитория
git clone https://github.com/your-username/chatbot-project.git
cd chatbot-project
```

### Через скачивание архива
1. Скачайте ZIP архив проекта
2. Распакуйте в нужную папку
3. Откройте терминал в этой папке

---

## ⚙️ Шаг 3: Настройка переменных окружения

### Создание файла .env
```bash
# Скопируйте пример конфигурации
cp env.example .env
```

### Редактирование .env файла
Откройте файл `.env` в текстовом редакторе и заполните:

```env
# Telegram Bot Configuration
BOT_TOKEN=your_telegram_bot_token_here

# Database Configuration  
DB_URI=postgresql://bot_user:bot_password_123@postgres:5432/telegram_bot

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Google AI Configuration
GEMINI_EMBEDD=your_google_ai_api_key_here
EMBEDDING_MODEL=gemini-embedding-001

# Memory Settings
MAX_MESSAGES=20
MAX_TOKENS=4000
LIMIT_SEARCH_EMBEDDINGS=3

# Database Tables
TABLE_EMBEDDNAME=embeddings
```

### 🔑 Получение API ключей

#### Telegram Bot Token
1. Откройте [@BotFather](https://t.me/botfather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен

#### OpenAI API Key
1. Зайдите на [platform.openai.com](https://platform.openai.com)
2. Войдите в аккаунт или создайте новый
3. Перейдите в API Keys
4. Создайте новый ключ
5. Скопируйте ключ (начинается с `sk-`)

#### Google AI API Key
1. Зайдите на [aistudio.google.com](https://aistudio.google.com)
2. Войдите в аккаунт Google
3. Перейдите в API Keys
4. Создайте новый ключ
5. Скопируйте ключ

---

## 🚀 Шаг 4: Запуск проекта

### Быстрый запуск (рекомендуется)
```bash
# Запуск всех сервисов одной командой
docker-compose up -d
```

### Пошаговый запуск
```bash
# 1. Скачивание готового образа бота
docker pull dedzyuka/chatbot:latest

# 2. Запуск базы данных PostgreSQL
docker run -d --name postgres-bot \
  -e POSTGRES_DB=telegram_bot \
  -e POSTGRES_USER=bot_user \
  -e POSTGRES_PASSWORD=bot_password_123 \
  -p 5432:5432 \
  postgres:13

# 3. Запуск бота
docker run -d --name chatbot \
  --env-file .env \
  --link postgres-bot:postgres \
  dedzyuka/chatbot:latest
```

---

## ✅ Шаг 5: Проверка работы

### Проверка статуса контейнеров
```bash
# Просмотр запущенных контейнеров
docker ps

# Должно показать что-то вроде:
# CONTAINER ID   IMAGE                    COMMAND                  CREATED         STATUS         PORTS                    NAMES
# abc123def456   dedzyuka/chatbot:latest  "python main.py"         2 minutes ago   Up 2 minutes   0.0.0.0:8080->8080/tcp   chatbot
# def456ghi789   postgres:13              "docker-entrypoint.s…"   2 minutes ago   Up 2 minutes   0.0.0.0:5432->5432/tcp   postgres-bot
```

### Проверка логов бота
```bash
# Просмотр логов бота
docker logs chatbot

# Просмотр логов в реальном времени
docker logs -f chatbot
```

### Проверка в Telegram
1. Найдите своего бота в Telegram
2. Отправьте команду `/start`
3. Бот должен ответить приветствием

---

## 🔧 Шаг 6: Управление проектом

### Основные команды

```bash
# Остановка всех сервисов
docker-compose down

# Перезапуск сервисов
docker-compose restart

# Просмотр логов
docker-compose logs -f bot

# Обновление до последней версии
docker-compose pull
docker-compose up -d
```

### Управление через Makefile
```bash
# Показать все доступные команды
make help

# Быстрый запуск
make quick

# Просмотр статуса
make status

# Остановка
make stop

# Просмотр логов
make logs
```

---

## 🌐 Шаг 7: Веб-интерфейсы

### pgAdmin (управление базой данных)
- **URL**: http://localhost:8080
- **Email**: admin@example.com
- **Пароль**: admin

#### Подключение к базе данных в pgAdmin:
1. Откройте pgAdmin
2. Добавьте новый сервер:
   - **Host**: postgres
   - **Port**: 5432
   - **Database**: telegram_bot
   - **Username**: bot_user
   - **Password**: bot_password_123

---

## 🛠️ Решение проблем

### Проблема: Бот не отвечает
```bash
# Проверьте логи
docker logs chatbot

# Перезапустите бота
docker restart chatbot
```

### Проблема: Ошибки подключения к БД
```bash
# Проверьте статус PostgreSQL
docker logs postgres-bot

# Перезапустите базу данных
docker restart postgres-bot
```

### Проблема: Неверные API ключи
1. Проверьте файл `.env`
2. Убедитесь, что ключи скопированы полностью
3. Перезапустите бота после изменений

### Проблема: Порты заняты
```bash
# Проверьте какие порты используются
netstat -tulpn | grep :5432
netstat -tulpn | grep :8080

# Остановите конфликтующие сервисы или измените порты в docker-compose.yml
```

---

## 📊 Мониторинг и логи

### Просмотр логов
```bash
# Логи бота
docker logs -f chatbot

# Логи базы данных
docker logs -f postgres-bot

# Логи всех сервисов
docker-compose logs -f
```

### Проверка использования ресурсов
```bash
# Статистика контейнеров
docker stats

# Информация о дисках
docker system df
```

---

## 🔄 Обновление проекта

### Обновление до новой версии
```bash
# Остановка сервисов
docker-compose down

# Скачивание новой версии
docker-compose pull

# Запуск обновленной версии
docker-compose up -d
```

### Обновление исходного кода
```bash
# Получение обновлений из Git
git pull origin main

# Пересборка и запуск
docker-compose up -d --build
```

---

## 🗑️ Удаление проекта

### Полное удаление
```bash
# Остановка и удаление контейнеров
docker-compose down

# Удаление образов
docker rmi dedzyuka/chatbot:latest
docker rmi postgres:13

# Удаление данных базы данных
docker volume rm chatbot_postgres_data

# Удаление папки проекта
rm -rf chatbot-project
```

---

## 📞 Поддержка

### Полезные ссылки
- **Docker Hub**: https://hub.docker.com/r/dedzyuka/chatbot
- **GitHub**: https://github.com/your-username/chatbot-project
- **Telegram Bot API**: https://core.telegram.org/bots/api

### Логи и отладка
```bash
# Подробные логи с временными метками
docker logs -f --timestamps chatbot

# Проверка конфигурации
docker exec chatbot python -c "from bot.config import *; print('Config loaded successfully')"
```

---

## 🎉 Готово!

Ваш AI Telegram бот с памятью запущен и готов к работе!

**Основные возможности:**
- ✅ Краткосрочная память (контекст диалога)
- ✅ Долгосрочная память (запоминание между сессиями)
- ✅ Векторный поиск по базе знаний
- ✅ Персонализация для каждого пользователя
- ✅ Автоматическая суммаризация старых сообщений

**Команды для управления:**
- `make help` - показать все команды
- `make logs` - просмотр логов
- `make status` - статус сервисов
- `make stop` - остановка
- `make restart` - перезапуск

Удачного использования! 🚀
