# 📤 Инструкция для отправки проекта пользователю

## 🎯 **Что отправить человеку без файлов проекта:**

### **Вариант 1: Минимальный пакет (рекомендуется)**

**Отправьте:**
1. **Архив**: `chatbot-minimal-package.zip` (10KB) или `chatbot-minimal-package.tar.gz` (7KB)
2. **Ссылку**: https://hub.docker.com/r/dedzyuka/chatbot

**Инструкция для пользователя:**
```
🤖 AI Telegram Bot - Установка

1. Скачайте архив: chatbot-minimal-package.zip
2. Распакуйте архив
3. Запустите:
   - Linux/Mac: ./install.sh
   - Windows: install.bat
4. Отредактируйте .env файл с API ключами
5. Готово! Бот запущен!

Готовый образ: https://hub.docker.com/r/dedzyuka/chatbot
```

---

### **Вариант 2: GitHub репозиторий**

**Отправьте ссылку:**
```
https://github.com/your-username/chatbot-project
```

**Инструкция:**
```
git clone https://github.com/your-username/chatbot-project.git
cd chatbot-project
./install.sh
```

---

### **Вариант 3: Только Docker образ**

**Отправьте:**
```
docker run -d --name chatbot \
  -e BOT_TOKEN=your_token \
  -e OPENAI_API_KEY=your_key \
  -e GEMINI_EMBEDD=your_key \
  -e DB_URI=postgresql://bot_user:bot_password_123@host:5432/telegram_bot \
  dedzyuka/chatbot:latest
```

---

## 📋 **Что включено в минимальный пакет:**

- ✅ `docker-compose.yml` - конфигурация сервисов
- ✅ `env.example` - пример переменных окружения
- ✅ `install.sh` - автоматическая установка (Linux/Mac)
- ✅ `install.bat` - автоматическая установка (Windows)
- ✅ `QUICK_START.md` - быстрый старт за 5 минут
- ✅ `INSTALLATION_GUIDE.md` - подробная инструкция
- ✅ `README.md` - описание пакета

---

## 🔑 **Что нужно пользователю:**

### **Обязательные API ключи:**
1. **Telegram Bot Token**
   - Создать бота через [@BotFather](https://t.me/botfather)
   - Получить токен

2. **OpenAI API Key**
   - Зарегистрироваться на [platform.openai.com](https://platform.openai.com)
   - Создать API ключ

3. **Google AI API Key**
   - Зарегистрироваться на [aistudio.google.com](https://aistudio.google.com)
   - Создать API ключ

### **Системные требования:**
- Docker Desktop (Windows/Mac) или Docker (Linux)
- 4GB+ RAM
- 2GB+ свободного места
- Интернет соединение

---

## 📞 **Поддержка пользователя:**

### **Частые вопросы:**

**Q: Бот не отвечает**
```bash
docker logs chatbot
docker restart chatbot
```

**Q: Ошибки подключения к БД**
```bash
docker logs postgres-bot
docker restart postgres-bot
```

**Q: Неверные API ключи**
- Проверить файл `.env`
- Перезапустить бота

**Q: Порты заняты**
```bash
# Изменить порты в docker-compose.yml
# Или остановить конфликтующие сервисы
```

### **Полезные команды:**
```bash
docker ps                    # статус контейнеров
docker logs -f chatbot      # логи бота
docker-compose restart      # перезапуск
docker-compose stop         # остановка
docker-compose up -d        # запуск
```

---

## 🎉 **Результат:**

Пользователь получит:
- ✅ Работающий AI Telegram бот
- ✅ Краткосрочную память (контекст диалога)
- ✅ Долгосрочную память (запоминание между сессиями)
- ✅ Векторный поиск по базе знаний
- ✅ Веб-интерфейс для управления БД (pgAdmin)
- ✅ Автоматическую установку и настройку

**Время установки: 5-10 минут**
