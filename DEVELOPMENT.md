# 👨‍💻 Руководство разработчика

## 🚀 Начало разработки

### Требования
- **Python 3.11+**
- **Git**
- **SQLite/PostgreSQL/MySQL**
- **Telegram Bot Token**

### Установка окружения
```bash
# Клонирование репозитория
git clone <repository-url>
cd tztgbot

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/macOS
# или
venv\Scripts\activate     # Windows

# Установка зависимостей
pip install -r requirements.txt
```

### Настройка проекта
```bash
# Копирование конфигурации
cp env.example .env

# Редактирование конфигурации
nano .env  # или любой другой редактор
```

## 🏗️ Архитектура проекта

### Структура файлов
```
tztgbot/
├── bot.py              # Основное приложение
├── config.py           # Конфигурация
├── database.py         # Модели БД
├── models.py           # Pydantic модели
├── services.py         # Бизнес-логика
├── handlers.py         # Обработчики сообщений
├── keyboards.py        # Inline клавиатуры
├── utils.py            # Утилиты
├── init_db.py          # Инициализация БД
├── tests.py            # Unit тесты
├── run_bot.py          # Скрипт запуска
├── run_tests.py        # Скрипт тестов
└── requirements.txt    # Зависимости
```

### Принципы архитектуры
- **Separation of Concerns** - Разделение ответственности
- **Single Responsibility** - Один класс - одна задача
- **Dependency Injection** - Внедрение зависимостей
- **Repository Pattern** - Паттерн репозитория
- **Service Layer** - Слой сервисов

## 🔧 Разработка

### Добавление новой функции

#### 1. Создание модели
```python
# models.py
class NewFeatureCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

class NewFeatureResponse(NewFeatureCreate):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
```

#### 2. Создание модели БД
```python
# database.py
class NewFeature(Base):
    __tablename__ = "new_features"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

#### 3. Создание сервиса
```python
# services.py
class NewFeatureService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_feature(self, feature_data: NewFeatureCreate) -> NewFeature:
        feature = NewFeature(**feature_data.dict())
        self.db.add(feature)
        self.db.commit()
        self.db.refresh(feature)
        return feature
```

#### 4. Добавление обработчика
```python
# handlers.py
async def handle_new_feature(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик новой функции"""
    # Логика обработки
    pass
```

#### 5. Создание клавиатуры
```python
# keyboards.py
@staticmethod
def new_feature_keyboard():
    """Клавиатура для новой функции"""
    keyboard = [
        [InlineKeyboardButton("Новая функция", callback_data="new_feature")]
    ]
    return InlineKeyboardMarkup(keyboard)
```

#### 6. Написание тестов
```python
# tests.py
class TestNewFeatureService:
    def test_create_feature(self, db_session):
        """Тест создания новой функции"""
        service = NewFeatureService(db_session)
        feature_data = NewFeatureCreate(name="Test Feature")
        
        feature = service.create_feature(feature_data)
        
        assert feature.name == "Test Feature"
        assert feature.id is not None
```

### Стиль кода

#### PEP 8
```python
# Хорошо
def calculate_total_price(items: List[CartItem]) -> float:
    """Calculate total price for cart items."""
    return sum(item.quantity * item.product.price for item in items)

# Плохо
def calcTotal(items):
    total=0
    for item in items:
        total+=item.quantity*item.product.price
    return total
```

#### Типизация
```python
from typing import List, Optional, Dict, Any

def process_order(
    order_id: int,
    items: List[OrderItem],
    metadata: Optional[Dict[str, Any]] = None
) -> Order:
    """Process order with type hints."""
    pass
```

#### Документация
```python
def create_user(user_data: UserCreate) -> User:
    """
    Create a new user in the database.
    
    Args:
        user_data: User creation data
        
    Returns:
        Created user object
        
    Raises:
        ValueError: If user data is invalid
        IntegrityError: If user already exists
    """
    pass
```

### Обработка ошибок

#### Try-catch блоки
```python
async def safe_operation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Безопасная операция с обработкой ошибок"""
    try:
        # Основная логика
        result = await self.perform_operation()
        await update.message.reply_text(f"Результат: {result}")
        
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        await update.message.reply_text("Ошибка валидации данных")
        
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        await update.message.reply_text("Ошибка базы данных")
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        await update.message.reply_text("Произошла неожиданная ошибка")
```

#### Валидация данных
```python
def validate_user_input(text: str) -> bool:
    """Validate user input"""
    if not text or len(text.strip()) == 0:
        return False
    
    if len(text) > 1000:
        return False
    
    # Дополнительные проверки
    return True
```

### Логирование

#### Настройка логирования
```python
import logging
from loguru import logger

# Настройка логирования
logger.add(
    "logs/bot.log",
    rotation="1 day",
    retention="30 days",
    level="INFO"
)

# Использование
logger.info("User started bot")
logger.error(f"Error processing order: {error}")
logger.debug(f"Debug info: {data}")
```

#### Структурированное логирование
```python
logger.info(
    "Order created",
    extra={
        "order_id": order.id,
        "user_id": user.id,
        "total_amount": order.total_amount
    }
)
```

## 🧪 Тестирование

### Запуск тестов
```bash
# Все тесты
python run_tests.py

# Конкретный тест
python run_tests.py test:TestCategoryService

# С покрытием
python run_tests.py coverage
```

### Написание тестов

#### Unit тесты
```python
def test_service_method(self, db_session):
    """Тест метода сервиса"""
    service = CategoryService(db_session)
    
    # Подготовка данных
    category_data = CategoryCreate(name="Test")
    
    # Выполнение
    result = service.create_category(category_data)
    
    # Проверка
    assert result.name == "Test"
    assert result.id is not None
```

#### Интеграционные тесты
```python
def test_full_workflow(self, db_session):
    """Тест полного рабочего процесса"""
    # Создание всех необходимых компонентов
    category_service = CategoryService(db_session)
    product_service = ProductService(db_session)
    
    # Выполнение полного процесса
    category = category_service.create_category(category_data)
    product = product_service.create_product(product_data)
    
    # Проверка результата
    assert category.id == product.category_id
```

#### Мокирование
```python
@patch('services.external_api.call')
def test_with_mock(self, mock_api_call):
    """Тест с мокированием"""
    mock_api_call.return_value = {"status": "success"}
    
    result = service.call_external_api()
    
    assert result["status"] == "success"
    mock_api_call.assert_called_once()
```

### Покрытие кода
```bash
# Генерация отчета
coverage run -m pytest tests.py
coverage report
coverage html

# Просмотр отчета
open htmlcov/index.html
```

## 🚀 Развертывание

### Локальное развертывание
```bash
# Запуск бота
python run_bot.py

# Проверка статуса
ps aux | grep python
```

### Продакшен развертывание
```bash
# Создание systemd сервиса
sudo nano /etc/systemd/system/ecommerce-bot.service

# Запуск сервиса
sudo systemctl start ecommerce-bot
sudo systemctl enable ecommerce-bot
```

### Docker развертывание
```bash
# Сборка образа
docker build -t ecommerce-bot .

# Запуск контейнера
docker run -d --name bot ecommerce-bot
```

## 🔍 Отладка

### Логирование
```python
# Включение отладочного режима
DEBUG=True
LOG_LEVEL=DEBUG

# Просмотр логов
tail -f logs/bot.log
```

### Отладка в коде
```python
import pdb

def debug_function():
    # Установка точки останова
    pdb.set_trace()
    
    # Код для отладки
    pass
```

### Мониторинг
```python
# Мониторинг производительности
import time

start_time = time.time()
# Выполнение операции
end_time = time.time()

logger.info(f"Operation took {end_time - start_time:.2f} seconds")
```

## 📊 Производительность

### Оптимизация запросов
```python
# Плохо - N+1 проблема
for order in orders:
    print(order.user.username)  # Отдельный запрос для каждого заказа

# Хорошо - eager loading
orders = db.query(Order).options(joinedload(Order.user)).all()
for order in orders:
    print(order.user.username)  # Данные уже загружены
```

### Кэширование
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_category_by_id(category_id: int) -> Category:
    """Кэшированное получение категории"""
    return db.query(Category).filter(Category.id == category_id).first()
```

### Асинхронность
```python
import asyncio

async def process_multiple_orders(orders: List[Order]):
    """Асинхронная обработка заказов"""
    tasks = [process_order(order) for order in orders]
    results = await asyncio.gather(*tasks)
    return results
```

## 🔒 Безопасность

### Валидация входных данных
```python
from pydantic import BaseModel, validator

class UserInput(BaseModel):
    name: str
    email: str
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v
```

### Санитизация данных
```python
import html

def sanitize_input(text: str) -> str:
    """Санитизация пользовательского ввода"""
    return html.escape(text.strip())
```

### Ограничение доступа
```python
def require_admin(func):
    """Декоратор для проверки прав администратора"""
    async def wrapper(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != settings.admin_user_id:
            await update.message.reply_text("Доступ запрещен")
            return
        return await func(self, update, context)
    return wrapper
```

## 📚 Документация

### Документирование кода
```python
def complex_function(param1: str, param2: int) -> Dict[str, Any]:
    """
    Выполняет сложную операцию с параметрами.
    
    Args:
        param1: Строковый параметр с описанием
        param2: Числовой параметр с описанием
        
    Returns:
        Словарь с результатами операции
        
    Raises:
        ValueError: Если параметры невалидны
        RuntimeError: Если операция не может быть выполнена
        
    Example:
        >>> result = complex_function("test", 42)
        >>> print(result["status"])
        "success"
    """
    pass
```

### Обновление документации
1. Обновляйте docstrings при изменении функций
2. Ведите CHANGELOG.md для отслеживания изменений
3. Обновляйте README.md при добавлении новых функций
4. Документируйте API изменения

## 🤝 Участие в разработке

### Workflow
1. **Fork** репозитория
2. Создайте **feature branch**
3. Внесите изменения с **тестами**
4. Создайте **Pull Request**
5. Пройдите **code review**

### Code Review
- Проверяйте код на соответствие стандартам
- Убедитесь в наличии тестов
- Проверяйте документацию
- Тестируйте функциональность

### Коммиты
```bash
# Хорошие сообщения коммитов
git commit -m "feat: add user registration functionality"
git commit -m "fix: resolve cart calculation bug"
git commit -m "docs: update API documentation"

# Плохие сообщения
git commit -m "fix"
git commit -m "update"
git commit -m "changes"
```

---

**Следуйте этим рекомендациям для эффективной разработки и поддержки проекта!**
