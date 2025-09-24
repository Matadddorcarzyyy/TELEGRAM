# 🚀 Быстрый старт

## Установка и запуск за 5 минут

### 1. Клонирование и установка зависимостей
```bash
git clone <repository-url>
cd tztgbot
pip install -r requirements.txt
```

### 2. Настройка бота
```bash
# Скопируйте файл с примером переменных окружения
cp env.example .env

# Отредактируйте .env файл
nano .env
```

Заполните в файле `.env`:
```env
BOT_TOKEN=your_bot_token_here
ADMIN_USER_ID=your_admin_user_id_here
```

### 3. Получение токена бота
1. Найдите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте токен в `.env`

### 4. Получение ID администратора
1. Найдите [@userinfobot](https://t.me/userinfobot)
2. Отправьте любое сообщение
3. Скопируйте ваш ID в `.env`

### 5. Запуск бота
```bash
python run_bot.py
```

Бот автоматически:
- ✅ Проверит все зависимости
- ✅ Инициализирует базу данных
- ✅ Добавит тестовые данные
- ✅ Запустится и будет готов к работе

## Тестирование

### Запуск тестов
```bash
python run_tests.py
```

### Запуск с покрытием кода
```bash
python run_tests.py coverage
```

## Основные команды

### Для пользователей:
- `/start` - Начать работу
- `/help` - Справка
- `/cart` - Показать корзину
- `/orders` - Мои заказы

### Для администраторов:
- `/admin` - Панель администратора

## Структура проекта

```
tztgbot/
├── bot.py              # Основной файл бота
├── run_bot.py          # Скрипт запуска с проверками
├── run_tests.py        # Скрипт запуска тестов
├── config.py           # Конфигурация
├── database.py         # Модели БД
├── models.py           # Pydantic модели
├── services.py         # Бизнес-логика
├── handlers.py         # Обработчики сообщений
├── keyboards.py        # Inline клавиатуры
├── utils.py            # Утилиты
├── init_db.py          # Инициализация БД
├── tests.py            # Unit тесты
├── requirements.txt    # Зависимости
├── .env                # Переменные окружения (создать)
├── env.example         # Пример переменных
├── README.md           # Полная документация
├── DATABASE_SETUP.md   # Настройка БД
├── API_EXAMPLES.md     # Примеры API
└── QUICK_START.md      # Этот файл
```

## Возможные проблемы

### Ошибка "Module not found"
```bash
pip install -r requirements.txt
```

### Ошибка "Bot token not found"
Проверьте файл `.env` и убедитесь, что `BOT_TOKEN` заполнен

### Ошибка "Database not found"
Бот автоматически предложит инициализировать БД при первом запуске

### Ошибка "Permission denied"
```bash
chmod +x run_bot.py
chmod +x run_tests.py
```

## Демо-данные

После инициализации БД будут добавлены:
- 5 категорий товаров
- 15 товаров в разных категориях
- Готовые для тестирования данные

## Поддержка

Если возникли проблемы:
1. Проверьте логи в `logs/bot.log`
2. Запустите тесты: `python run_tests.py`
3. Проверьте переменные окружения в `.env`
4. Создайте Issue в репозитории

---

**Готово! Ваш бот запущен и готов к работе! 🎉**
