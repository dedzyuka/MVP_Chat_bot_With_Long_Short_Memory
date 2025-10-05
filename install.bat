@echo off
setlocal enabledelayedexpansion

echo 🤖 AI Telegram Bot - Автоматическая установка
echo ==============================================

REM Проверка Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker не установлен!
    echo 📥 Установите Docker Desktop: https://docs.docker.com/get-docker/
    pause
    exit /b 1
)

echo ✅ Docker найден

REM Проверка docker-compose
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ docker-compose не найден!
    echo 📥 Установите docker-compose
    pause
    exit /b 1
)

echo ✅ docker-compose найден

REM Создание .env файла
if not exist .env (
    echo 📝 Создание файла .env...
    copy env.example .env
    echo ⚠️  ВАЖНО: Отредактируйте файл .env с вашими API ключами!
    echo    notepad .env
    echo.
    echo Обязательные ключи:
    echo    - BOT_TOKEN (получить у @BotFather)
    echo    - OPENAI_API_KEY (получить на platform.openai.com)
    echo    - GEMINI_EMBEDD (получить на aistudio.google.com)
    echo.
    pause
)

REM Скачивание образа
echo 📥 Скачивание образа dedzyuka/chatbot:latest...
docker pull dedzyuka/chatbot:latest

REM Запуск сервисов
echo 🚀 Запуск сервисов...
docker-compose up -d

REM Ожидание запуска
echo ⏳ Ожидание запуска сервисов...
timeout /t 10 /nobreak >nul

REM Проверка статуса
echo 📊 Проверка статуса...
docker ps | findstr chatbot >nul
if errorlevel 1 (
    echo ❌ Ошибка запуска сервисов
    echo 📋 Проверьте логи:
    echo    docker logs chatbot
    echo    docker logs postgres-bot
    pause
    exit /b 1
)

docker ps | findstr postgres >nul
if errorlevel 1 (
    echo ❌ Ошибка запуска сервисов
    echo 📋 Проверьте логи:
    echo    docker logs chatbot
    echo    docker logs postgres-bot
    pause
    exit /b 1
)

echo ✅ Все сервисы запущены успешно!
echo.
echo 🎉 Бот готов к работе!
echo.
echo 📋 Полезные команды:
echo    docker logs -f chatbot    # Просмотр логов
echo    docker-compose stop       # Остановка
echo    docker-compose restart    # Перезапуск
echo.
echo 🌐 Веб-интерфейсы:
echo    pgAdmin: http://localhost:8080 (admin@example.com / admin)
echo.
echo 📱 Найдите своего бота в Telegram и отправьте /start

pause
