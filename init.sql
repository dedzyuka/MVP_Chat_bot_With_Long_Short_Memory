-- Инициализация базы данных для Telegram Bot
-- Этот файл выполняется автоматически при первом запуске PostgreSQL в Docker

-- Создание расширений для векторного поиска
CREATE EXTENSION IF NOT EXISTS vector;

-- Создание пользователя (если не существует)
-- DO $$
-- BEGIN
--     IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'bot_user') THEN
--         CREATE ROLE bot_user LOGIN PASSWORD 'bot_password_123';
--     END IF;
-- END
-- $$;

-- Предоставление прав
GRANT ALL PRIVILEGES ON DATABASE telegram_bot TO bot_user;

-- Создание таблицы для эмбеддингов (если нужна)
-- CREATE TABLE IF NOT EXISTS embeddings (
--     id SERIAL PRIMARY KEY,
--     content TEXT NOT NULL,
--     embedding vector(768),
--     metadata JSONB,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- Создание индекса для векторного поиска
-- CREATE INDEX IF NOT EXISTS embeddings_embedding_idx ON embeddings 
-- USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Комментарии для документации
COMMENT ON DATABASE telegram_bot IS 'База данных для AI Telegram Bot с памятью';
