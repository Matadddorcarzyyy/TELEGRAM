# 🗄️ Инструкция по настройке базы данных

## Обзор

Проект использует SQLAlchemy ORM с поддержкой различных типов баз данных. По умолчанию настроена SQLite для простоты разработки и тестирования.

## Поддерживаемые СУБД

- ✅ **SQLite** (по умолчанию) - для разработки и тестирования
- ✅ **PostgreSQL** - для продакшена
- ✅ **MySQL** - для продакшена
- ✅ **MariaDB** - для продакшена

## Быстрая настройка (SQLite)

### 1. Автоматическая инициализация
```bash
python init_db.py
```

Этот скрипт:
- Создаст все необходимые таблицы
- Добавит тестовые данные (категории и товары)
- Настроит связи между таблицами

### 2. Ручная инициализация
```python
from database import create_tables
create_tables()
```

## Настройка PostgreSQL

### 1. Установка зависимостей
```bash
pip install psycopg2-binary
# или
pip install psycopg2
```

### 2. Настройка переменных окружения
```env
DATABASE_URL=postgresql://username:password@localhost:5432/ecommerce_bot
```

### 3. Создание базы данных
```sql
CREATE DATABASE ecommerce_bot;
CREATE USER bot_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE ecommerce_bot TO bot_user;
```

### 4. Инициализация
```bash
python init_db.py
```

## Настройка MySQL/MariaDB

### 1. Установка зависимостей
```bash
pip install PyMySQL
# или
pip install mysqlclient
```

### 2. Настройка переменных окружения
```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/ecommerce_bot
```

### 3. Создание базы данных
```sql
CREATE DATABASE ecommerce_bot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'bot_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON ecommerce_bot.* TO 'bot_user'@'localhost';
FLUSH PRIVILEGES;
```

### 4. Инициализация
```bash
python init_db.py
```

## Структура базы данных

### Диаграмма связей
```
users (1) -----> (N) cart_items (N) <----- (1) products
  |                                           |
  |                                           |
  v                                           v
orders (1) -----> (N) order_items (N) <----- (1) products
  |
  v
categories (1) -----> (N) products
```

### Описание таблиц

#### 1. categories - Категории товаров
```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Поля:**
- `id` - Уникальный идентификатор
- `name` - Название категории (уникальное)
- `description` - Описание категории
- `is_active` - Активна ли категория
- `created_at` - Дата создания

#### 2. products - Товары
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price FLOAT NOT NULL,
    photo_url VARCHAR(500),
    stock_quantity INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    category_id INTEGER REFERENCES categories(id),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Поля:**
- `id` - Уникальный идентификатор
- `name` - Название товара
- `description` - Описание товара
- `price` - Цена товара
- `photo_url` - URL фотографии товара
- `stock_quantity` - Количество на складе
- `is_active` - Активен ли товар
- `category_id` - Ссылка на категорию
- `created_at` - Дата создания

#### 3. users - Пользователи
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE NOT NULL,
    username VARCHAR(100),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Поля:**
- `id` - Уникальный идентификатор
- `telegram_id` - ID пользователя в Telegram (уникальный)
- `username` - Имя пользователя в Telegram
- `first_name` - Имя
- `last_name` - Фамилия
- `phone` - Телефон
- `address` - Адрес
- `created_at` - Дата регистрации

#### 4. cart_items - Элементы корзины
```sql
CREATE TABLE cart_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Поля:**
- `id` - Уникальный идентификатор
- `user_id` - Ссылка на пользователя
- `product_id` - Ссылка на товар
- `quantity` - Количество товара
- `created_at` - Дата добавления

#### 5. orders - Заказы
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number VARCHAR(20) UNIQUE NOT NULL,
    user_id INTEGER REFERENCES users(id),
    total_amount FLOAT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    delivery_method VARCHAR(50),
    delivery_address TEXT,
    customer_name VARCHAR(100),
    customer_phone VARCHAR(20),
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);
```

**Поля:**
- `id` - Уникальный идентификатор
- `order_number` - Номер заказа (уникальный)
- `user_id` - Ссылка на пользователя
- `total_amount` - Общая сумма заказа
- `status` - Статус заказа
- `delivery_method` - Способ доставки
- `delivery_address` - Адрес доставки
- `customer_name` - Имя клиента
- `customer_phone` - Телефон клиента
- `notes` - Примечания к заказу
- `created_at` - Дата создания
- `updated_at` - Дата обновления

#### 6. order_items - Элементы заказов
```sql
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    price FLOAT NOT NULL
);
```

**Поля:**
- `id` - Уникальный идентификатор
- `order_id` - Ссылка на заказ
- `product_id` - Ссылка на товар
- `quantity` - Количество товара
- `price` - Цена товара на момент заказа

## Статусы заказов

- `pending` - Ожидает подтверждения
- `confirmed` - Подтвержден
- `shipped` - Отправлен
- `delivered` - Доставлен
- `cancelled` - Отменен

## Способы доставки

- `pickup` - Самовывоз
- `courier` - Курьерская доставка
- `post` - Почтовая доставка

## Миграции базы данных

### Создание миграции
```bash
alembic revision --autogenerate -m "Initial migration"
```

### Применение миграций
```bash
alembic upgrade head
```

### Откат миграций
```bash
alembic downgrade -1
```

## Резервное копирование

### SQLite
```bash
cp ecommerce_bot.db ecommerce_bot_backup_$(date +%Y%m%d_%H%M%S).db
```

### PostgreSQL
```bash
pg_dump -h localhost -U bot_user ecommerce_bot > backup_$(date +%Y%m%d_%H%M%S).sql
```

### MySQL
```bash
mysqldump -u bot_user -p ecommerce_bot > backup_$(date +%Y%m%d_%H%M%S).sql
```

## Восстановление из резервной копии

### SQLite
```bash
cp ecommerce_bot_backup_20231201_120000.db ecommerce_bot.db
```

### PostgreSQL
```bash
psql -h localhost -U bot_user ecommerce_bot < backup_20231201_120000.sql
```

### MySQL
```bash
mysql -u bot_user -p ecommerce_bot < backup_20231201_120000.sql
```

## Мониторинг и оптимизация

### Проверка размера базы данных
```sql
-- SQLite
SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size();

-- PostgreSQL
SELECT pg_size_pretty(pg_database_size('ecommerce_bot'));

-- MySQL
SELECT ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'DB Size in MB'
FROM information_schema.tables WHERE table_schema = 'ecommerce_bot';
```

### Индексы для оптимизации
```sql
-- Индексы для часто используемых запросов
CREATE INDEX idx_users_telegram_id ON users(telegram_id);
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_products_is_active ON products(is_active);
CREATE INDEX idx_cart_items_user_id ON cart_items(user_id);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
```

## Устранение неполадок

### Проблема: База данных заблокирована
**Решение:** Убедитесь, что все соединения с БД закрыты, перезапустите приложение.

### Проблема: Ошибка подключения к PostgreSQL
**Решение:** Проверьте:
- Запущен ли PostgreSQL сервер
- Правильность параметров подключения
- Права доступа пользователя

### Проблема: Ошибка кодировки в MySQL
**Решение:** Убедитесь, что база данных создана с кодировкой `utf8mb4`.

### Проблема: Медленные запросы
**Решение:** 
- Добавьте индексы для часто используемых полей
- Оптимизируйте запросы
- Рассмотрите возможность партиционирования больших таблиц

## Безопасность

### Рекомендации:
1. Используйте отдельного пользователя БД для приложения
2. Ограничьте права доступа пользователя БД
3. Регулярно создавайте резервные копии
4. Используйте SSL для подключений к БД в продакшене
5. Не храните пароли БД в коде - используйте переменные окружения

### Пример настройки пользователя PostgreSQL:
```sql
-- Создание пользователя с ограниченными правами
CREATE USER bot_user WITH PASSWORD 'strong_password';
GRANT CONNECT ON DATABASE ecommerce_bot TO bot_user;
GRANT USAGE ON SCHEMA public TO bot_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO bot_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO bot_user;
```

---

**Примечание:** Всегда тестируйте изменения в базе данных на тестовой среде перед применением в продакшене!
