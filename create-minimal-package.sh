#!/bin/bash

# Создание минимального пакета для отправки пользователю
# Использование: ./create-minimal-package.sh

set -e

echo "📦 Создание минимального пакета для отправки..."

# Создание временной папки
PACKAGE_NAME="chatbot-minimal-package"
rm -rf $PACKAGE_NAME
mkdir $PACKAGE_NAME

# Копирование необходимых файлов
echo "📋 Копирование файлов..."

# Основные файлы конфигурации
cp docker-compose.yml $PACKAGE_NAME/
cp env.example $PACKAGE_NAME/
cp install.sh $PACKAGE_NAME/
cp install.bat $PACKAGE_NAME/

# Документация
cp QUICK_START.md $PACKAGE_NAME/
cp INSTALLATION_GUIDE.md $PACKAGE_NAME/

# Создание README для пакета
cat > $PACKAGE_NAME/README.md << 'EOF'
# 🤖 AI Telegram Bot - Минимальный пакет

Этот пакет содержит все необходимое для запуска AI Telegram бота с памятью.

## 🚀 Быстрый запуск

### Linux/Mac:
```bash
chmod +x install.sh
./install.sh
```

### Windows:
```cmd
install.bat
```

## 📋 Что включено

- ✅ Готовый Docker образ `dedzyuka/chatbot:latest`
- ✅ Автоматическая установка PostgreSQL
- ✅ Веб-интерфейс pgAdmin
- ✅ Настройка переменных окружения

## 🔑 Что нужно настроить

Отредактируйте файл `.env` и укажите:
- `BOT_TOKEN` - токен от @BotFather
- `OPENAI_API_KEY` - ключ от OpenAI
- `GEMINI_EMBEDD` - ключ от Google AI

## 📚 Документация

- `QUICK_START.md` - быстрый старт за 5 минут
- `INSTALLATION_GUIDE.md` - подробная инструкция

## 🆘 Поддержка

Если возникли проблемы:
1. Проверьте логи: `docker logs chatbot`
2. Убедитесь в правильности API ключей
3. Перезапустите: `docker-compose restart`

---

**Готовый образ**: https://hub.docker.com/r/dedzyuka/chatbot
EOF

# Создание архива
echo "🗜️ Создание архива..."
tar -czf ${PACKAGE_NAME}.tar.gz $PACKAGE_NAME
zip -r ${PACKAGE_NAME}.zip $PACKAGE_NAME

# Очистка
rm -rf $PACKAGE_NAME

echo "✅ Готово!"
echo ""
echo "📦 Созданные архивы:"
echo "   - ${PACKAGE_NAME}.tar.gz (Linux/Mac)"
echo "   - ${PACKAGE_NAME}.zip (Windows)"
echo ""
echo "📋 Размер архива:"
ls -lh ${PACKAGE_NAME}.*
echo ""
echo "📤 Отправьте один из архивов пользователю вместе с инструкцией:"
echo ""
echo "=== ИНСТРУКЦИЯ ДЛЯ ПОЛЬЗОВАТЕЛЯ ==="
echo "1. Скачайте архив: ${PACKAGE_NAME}.tar.gz (или .zip)"
echo "2. Распакуйте архив"
echo "3. Запустите: ./install.sh (Linux/Mac) или install.bat (Windows)"
echo "4. Отредактируйте .env файл с вашими API ключами"
echo "5. Готово! Бот запущен!"
echo ""
echo "🔗 Готовый образ: https://hub.docker.com/r/dedzyuka/chatbot"
