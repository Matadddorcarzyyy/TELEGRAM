# 🛍️ E-commerce Telegram Bot

Полнофункциональный Telegram бот для интернет-магазина с полным циклом покупки товаров.

## 📋 Функциональные возможности

### 🔹 Каталог товаров
- ✅ Отображение списка категорий товаров
- ✅ Просмотр товаров в выбранной категории
- ✅ Детальная информация о товаре (название, описание, цена, фото)
- ✅ Навигация через inline-клавиатуру

### 🔹 Корзина покупок
- ✅ Добавление товаров в корзину
- ✅ Просмотр содержимого корзины
- ✅ Изменение количества товаров
- ✅ Удаление товаров из корзины
- ✅ Подсчет общей стоимости

### 🔹 Оформление заказа
- ✅ Сбор контактных данных покупателя (имя, телефон, адрес)
- ✅ Выбор способа доставки
- ✅ Подтверждение заказа
- ✅ Генерация уникального номера заказа

### 🔹 Административная панель
- ✅ Команды для администратора (добавление/редактирование товаров)
- ✅ Просмотр списка заказов
- ✅ Изменение статуса заказа

## 🏗️ Архитектура проекта

```
tztgbot/
├── bot.py              # Основной файл бота
├── config.py           # Конфигурация приложения
├── database.py         # Модели базы данных
├── models.py           # Pydantic модели
├── services.py         # Бизнес-логика
├── handlers.py         # Обработчики сообщений и callback'ов
├── keyboards.py        # Inline клавиатуры
├── utils.py            # Утилиты и вспомогательные функции
├── init_db.py          # Инициализация БД с тестовыми данными
├── tests.py            # Unit тесты
├── requirements.txt    # Зависимости Python
└── README.md           # Документация
```

## 🚀 Установка и запуск

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd tztgbot
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Настройка окружения
Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

Заполните переменные окружения:
```env
BOT_TOKEN=your_bot_token_here
ADMIN_USER_ID=your_admin_user_id_here
DATABASE_URL=sqlite:///./ecommerce_bot.db
DEBUG=True
LOG_LEVEL=INFO
```

### 4. Инициализация базы данных
```bash
python init_db.py
```

### 5. Запуск бота
```bash
python bot.py
```

## 🔧 Настройка

### Получение токена бота
1. Найдите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен в файл `.env`

### Получение ID администратора
1. Найдите [@userinfobot](https://t.me/userinfobot) в Telegram
2. Отправьте любое сообщение
3. Скопируйте ваш ID в файл `.env`

## 📊 База данных

Проект использует SQLAlchemy с SQLite по умолчанию. Поддерживаются следующие модели:

### Основные таблицы:
- **categories** - Категории товаров
- **products** - Товары
- **users** - Пользователи
- **cart_items** - Элементы корзины
- **orders** - Заказы
- **order_items** - Элементы заказов

### Схема базы данных:
```sql
-- Категории
CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Товары
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price FLOAT NOT NULL,
    photo_url VARCHAR(500),
    stock_quantity INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    category_id INTEGER REFERENCES categories(id),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Пользователи
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    telegram_id INTEGER UNIQUE NOT NULL,
    username VARCHAR(100),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Корзина
CREATE TABLE cart_items (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Заказы
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
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

-- Элементы заказов
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    price FLOAT NOT NULL
);
```

## 🧪 Тестирование

Запуск тестов:
```bash
pytest tests.py -v
```

Тесты покрывают:
- ✅ Создание и управление категориями
- ✅ Создание и управление товарами
- ✅ Управление пользователями
- ✅ Функциональность корзины
- ✅ Создание и управление заказами
- ✅ Утилиты и валидация
- ✅ Интеграционные тесты

## 📱 Использование

### Команды бота:
- `/start` - Начать работу с ботом
- `/help` - Показать справку
- `/admin` - Панель администратора (только для админов)

### Основной функционал:
1. **Просмотр каталога** - Выберите категорию товаров
2. **Добавление в корзину** - Нажмите "Добавить в корзину" на товаре
3. **Управление корзиной** - Просмотр, изменение количества, удаление товаров
4. **Оформление заказа** - Заполните контактные данные и выберите доставку
5. **Отслеживание заказов** - Просмотр истории заказов

### Административные функции:
- Управление категориями товаров
- Управление товарами
- Просмотр и управление заказами
- Изменение статусов заказов

## 🔒 Безопасность

- Валидация всех входных данных
- Проверка прав администратора
- Обработка ошибок и исключений
- Логирование всех важных событий

## 📝 Логирование

Логи сохраняются в:
- Консоль (с цветовой подсветкой)
- Файл `logs/bot.log` (с ротацией)

Уровни логирования:
- `DEBUG` - Подробная отладочная информация
- `INFO` - Общая информация о работе
- `WARNING` - Предупреждения
- `ERROR` - Ошибки

## 🚀 Развертывание

### Локальное развертывание:
```bash
python bot.py
```

### Развертывание на сервере:
1. Установите зависимости
2. Настройте переменные окружения
3. Инициализируйте базу данных
4. Запустите бота с помощью systemd или supervisor

### Docker (опционально):
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "bot.py"]
```

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Добавьте тесты
5. Создайте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT.

## 📞 Поддержка

Если у вас возникли вопросы или проблемы:
1. Проверьте документацию
2. Запустите тесты
3. Проверьте логи
4. Создайте Issue в репозитории

## 🎯 Планы развития

- [ ] Интеграция с платежными системами
- [ ] Система скидок и промокодов
- [ ] Уведомления о статусе заказа
- [ ] Многоязычная поддержка
- [ ] API для внешних интеграций
- [ ] Система отзывов и рейтингов
- [ ] Аналитика и отчеты
- [ ] Мобильное приложение

---

**Создано с ❤️ для демонстрации возможностей Telegram Bot API**
