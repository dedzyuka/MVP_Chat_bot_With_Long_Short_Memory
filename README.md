# 🤖 AI Telegram Bot с Памятью

Интеллектуальный Telegram бот с краткосрочной и долгосрочной памятью, построенный на LangGraph и LangMem.

## 📋 Возможности

- **Краткосрочная память**: Сохранение контекста текущего диалога
- **Долгосрочная память**: Запоминание важной информации между сессиями
- **Векторный поиск**: Поиск релевантной информации в базе знаний
- **Персонализация**: Индивидуальный контекст для каждого пользователя
- **Суммаризация**: Автоматическое сжатие старых сообщений для экономии токенов

## 🏗️ Архитектура

```
bot/
├── main.py          # Точка входа, обработка Telegram сообщений
├── graph.py         # LangGraph workflow с долгосрочной памятью
├── memory.py        # Утилиты для управления краткосрочной памятью
├── config.py        # Конфигурация и переменные окружения
├── database.py      # Управление подключениями к PostgreSQL
└── embedd/          # Модуль векторного поиска
    ├── embeddsearch.py
    ├── newembeddsearch.py
    └── reqtoembedd.py
```

## 🚀 Быстрый старт

### ⚡ Автоматическая установка

**Linux/Mac:**
```bash
git clone <your-repo-url>
cd chatbot-project
chmod +x install.sh
./install.sh
```

**Windows:**
```cmd
git clone <your-repo-url>
cd chatbot-project
install.bat
```

### 📋 Ручная установка

**Предварительные требования:**
- Docker и docker-compose
- API ключи для OpenAI, Google AI и Telegram Bot

### 1. Клонирование репозитория

```bash
git clone <your-repo-url>
cd "project bot/MVP — копия 3"
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
# Telegram Bot
BOT_TOKEN=your_telegram_bot_token

# Database
DB_URI=postgresql://username:password@localhost:5432/database_name

# OpenAI
OPENAI_API_KEY=your_openai_api_key

# Google AI
GEMINI_EMBEDD=your_google_ai_api_key
EMBEDDING_MODEL=gemini-embedding-001

# Memory Settings
MAX_MESSAGES=20
MAX_TOKENS=4000
LIMIT_SEARCH_EMBEDDINGS=3

# Database Tables
TABLE_EMBEDDNAME=your_embeddings_table_name
```

### 5. Настройка базы данных

#### Вариант A: Локальная PostgreSQL

```bash
# Установка PostgreSQL (Ubuntu/Debian)
sudo apt-get install postgresql postgresql-contrib

# Создание базы данных
sudo -u postgres psql
CREATE DATABASE telegram_bot;
CREATE USER bot_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE telegram_bot TO bot_user;
\q
```

#### Вариант B: Docker PostgreSQL

```bash
# Запуск PostgreSQL в Docker
docker run --name postgres-bot \
  -e POSTGRES_DB=telegram_bot \
  -e POSTGRES_USER=bot_user \
  -e POSTGRES_PASSWORD=your_password \
  -p 5432:5432 \
  -d postgres:13

# Проверка подключения
docker exec -it postgres-bot psql -U bot_user -d telegram_bot
```

### 6. Инициализация таблиц

LangGraph и LangMem автоматически создадут необходимые таблицы при первом запуске.

### 7. Запуск бота

```bash
python main.py
```

## 🐳 Docker Deployment

### Docker Hub

Образ доступен в Docker Hub: `dedzyuka/chatbot`

```bash
# Быстрый запуск с готовым образом
docker run -d --name chatbot \
  -e BOT_TOKEN=your_token \
  -e OPENAI_API_KEY=your_key \
  -e GEMINI_EMBEDD=your_key \
  -e DB_URI=postgresql://user:pass@host:5432/db \
  dedzyuka/chatbot:latest
```

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Команда запуска
CMD ["python", "main.py"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: telegram_bot
      POSTGRES_USER: bot_user
      POSTGRES_PASSWORD: your_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U bot_user -d telegram_bot"]
      interval: 30s
      timeout: 10s
      retries: 3

  bot:
    build: .
    environment:
      - DB_URI=postgresql://bot_user:your_password@postgres:5432/telegram_bot
      - BOT_TOKEN=${BOT_TOKEN}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GEMINI_EMBEDD=${GEMINI_EMBEDD}
      - EMBEDDING_MODEL=gemini-embedding-001
      - MAX_MESSAGES=20
      - MAX_TOKENS=4000
      - LIMIT_SEARCH_EMBEDDINGS=3
      - TABLE_EMBEDDNAME=embeddings
    depends_on:
      postgres:
        condition: service_healthy
    restart: unless-stopped

volumes:
  postgres_data:
```

### Запуск с Docker Compose

```bash
# Создание .env файла
cp .env.example .env
# Отредактируйте .env с вашими ключами

# Запуск всех сервисов (использует готовый образ из Docker Hub)
docker-compose pull
docker-compose up -d

# Просмотр логов
docker-compose logs -f bot
```

### Сборка и деплой собственного образа

```bash
# Авторизация в Docker Hub
docker login

# Сборка и загрузка образа
./deploy.sh

# Или с указанием версии
./deploy.sh v1.0.0
```

## 📊 Мониторинг и логирование

### Просмотр логов

```bash
# Локальный запуск с подробными логами
python main.py

# Docker логи
docker-compose logs -f bot
```

### Проверка состояния базы данных

```bash
# Подключение к PostgreSQL
docker exec -it postgres-bot psql -U bot_user -d telegram_bot

# Просмотр таблиц
\dt

# Проверка данных памяти
SELECT * FROM langgraph_checkpoints LIMIT 5;
```

## 🔧 Конфигурация

### Настройки памяти

- `MAX_MESSAGES`: Максимальное количество сообщений в краткосрочной памяти
- `MAX_TOKENS`: Максимальное количество токенов для обработки
- `LIMIT_SEARCH_EMBEDDINGS`: Количество релевантных чанков для поиска

### Настройки поиска

- `EMBEDDING_MODEL`: Модель для создания эмбеддингов
- `TABLE_EMBEDDNAME`: Название таблицы с эмбеддингами

## 🚨 Устранение неполадок

### Частые проблемы

1. **Ошибка подключения к БД**
   ```bash
   # Проверьте строку подключения в .env
   DB_URI=postgresql://username:password@host:port/database
   ```

2. **Недоступны API ключи**
   ```bash
   # Проверьте переменные окружения
   echo $OPENAI_API_KEY
   echo $GEMINI_EMBEDD
   ```

3. **Ошибки импорта**
   ```bash
   # Переустановите зависимости
   pip install --force-reinstall -r requirements.txt
   ```

### Логи и отладка

```bash
# Включение подробного логирования
export PYTHONPATH=.
python -u main.py
```

## 📈 Производительность

### Рекомендации

- Используйте connection pooling для высокой нагрузки
- Настройте индексы в PostgreSQL для векторного поиска
- Мониторьте использование токенов OpenAI
- Регулярно очищайте старые checkpoint'ы

### Масштабирование

- Горизонтальное масштабирование: несколько инстансов бота
- Балансировка нагрузки через nginx
- Отдельный сервер для PostgreSQL в production

## 🤝 Разработка

### Структура проекта

- `bot/main.py` - Обработка Telegram сообщений
- `bot/graph.py` - LangGraph workflow
- `bot/memory.py` - Управление памятью
- `bot/embedd/` - Векторный поиск

### Добавление новых функций

1. Создайте новую ноду в `graph.py`
2. Добавьте обработчик в `main.py`
3. Обновите State типы
4. Протестируйте локально

## 📚 Дополнительная документация

- **[INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)** - Подробная инструкция по установке
- **[QUICK_START.md](QUICK_START.md)** - Быстрый старт за 5 минут
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Инструкции по деплою в Docker Hub

## 📄 Лицензия

MIT License

## 🆘 Поддержка

Если у вас возникли проблемы:

1. Проверьте логи приложения
2. Убедитесь в правильности конфигурации
3. Проверьте доступность внешних API
4. Создайте issue в репозитории

---

**Удачного использования! 🚀**
