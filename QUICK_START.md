# ⚡ Быстрый запуск AI Telegram Bot

## 🚀 За 5 минут до работающего бота

### 1. Установите Docker
- **Windows/Mac**: [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **Linux**: `curl -fsSL https://get.docker.com | sh`

### 2. Скачайте проект
```bash
git clone https://github.com/your-username/chatbot-project.git
cd chatbot-project
```

### 3. Настройте переменные
```bash
cp env.example .env
nano .env  # Отредактируйте файл с вашими API ключами
```

### 4. Запустите бота
```bash
docker-compose up -d
```

### 5. Проверьте работу
```bash
docker logs chatbot
```

---

## 🔑 Обязательные API ключи

В файле `.env` укажите:

```env
BOT_TOKEN=1234567890:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
OPENAI_API_KEY=sk-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
GEMINI_EMBEDD=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
```

**Где получить:**
- `BOT_TOKEN` → [@BotFather](https://t.me/botfather) в Telegram
- `OPENAI_API_KEY` → [platform.openai.com](https://platform.openai.com)
- `GEMINI_EMBEDD` → [aistudio.google.com](https://aistudio.google.com)

---

## ✅ Проверка

1. **Статус**: `docker ps` - должны быть запущены `chatbot` и `postgres`
2. **Логи**: `docker logs chatbot` - без ошибок
3. **Telegram**: Найдите бота и отправьте `/start`

---

## 🛠️ Полезные команды

```bash
# Остановить
docker-compose down

# Перезапустить  
docker-compose restart

# Обновить
docker-compose pull && docker-compose up -d

# Логи
docker logs -f chatbot
```

---

## 🆘 Если что-то не работает

1. **Проверьте API ключи** в `.env`
2. **Перезапустите**: `docker-compose restart`
3. **Посмотрите логи**: `docker logs chatbot`
4. **Проверьте порты**: `netstat -tulpn | grep :5432`

---

**Готово! Ваш бот работает! 🎉**
