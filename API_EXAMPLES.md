# 🔌 Примеры использования API

## Обзор

Данный документ содержит примеры использования сервисов и API бота для разработчиков.

## Импорт модулей

```python
from database import get_db_session
from services import CategoryService, ProductService, UserService, CartService, OrderService
from models import CategoryCreate, ProductCreate, UserCreate, OrderCreate, DeliveryMethod
```

## Работа с категориями

### Создание категории
```python
db = get_db_session()
category_service = CategoryService(db)

# Создание новой категории
category_data = CategoryCreate(
    name="Электроника",
    description="Смартфоны, планшеты, ноутбуки"
)
category = category_service.create_category(category_data)
print(f"Создана категория: {category.name}")
```

### Получение всех категорий
```python
categories = category_service.get_all_categories()
for category in categories:
    print(f"Категория: {category.name} - {category.description}")
```

### Обновление категории
```python
update_data = CategoryCreate(
    name="Обновленная электроника",
    description="Новое описание"
)
updated_category = category_service.update_category(category.id, update_data)
```

### Удаление категории (мягкое удаление)
```python
success = category_service.delete_category(category.id)
if success:
    print("Категория успешно удалена")
```

## Работа с товарами

### Создание товара
```python
product_service = ProductService(db)

product_data = ProductCreate(
    name="iPhone 15 Pro",
    description="Новейший смартфон от Apple",
    price=99990.0,
    photo_url="https://example.com/iphone.jpg",
    stock_quantity=10,
    category_id=category.id
)
product = product_service.create_product(product_data)
print(f"Создан товар: {product.name} за {product.price} ₽")
```

### Получение товаров по категории
```python
products = product_service.get_products_by_category(category.id)
for product in products:
    print(f"Товар: {product.name} - {product.price} ₽")
```

### Обновление товара
```python
update_data = ProductCreate(
    name="iPhone 15 Pro Max",
    price=109990.0,
    stock_quantity=5,
    category_id=category.id
)
updated_product = product_service.update_product(product.id, update_data)
```

### Поиск товара по ID
```python
product = product_service.get_product_by_id(product.id)
if product:
    print(f"Найден товар: {product.name}")
```

## Работа с пользователями

### Создание пользователя
```python
user_service = UserService(db)

user_data = UserCreate(
    telegram_id=12345,
    username="john_doe",
    first_name="John",
    last_name="Doe"
)
user = user_service.create_user(user_data)
print(f"Создан пользователь: {user.first_name} {user.last_name}")
```

### Получение или создание пользователя
```python
user = user_service.get_or_create_user(
    telegram_id=12345,
    username="john_doe",
    first_name="John",
    last_name="Doe"
)
```

### Обновление данных пользователя
```python
update_data = UserCreate(
    phone="+7(999)123-45-67",
    address="ул. Пушкина, д. 1"
)
updated_user = user_service.update_user(user.telegram_id, update_data)
```

### Поиск пользователя по Telegram ID
```python
user = user_service.get_user_by_telegram_id(12345)
if user:
    print(f"Пользователь найден: {user.username}")
```

## Работа с корзиной

### Добавление товара в корзину
```python
cart_service = CartService(db)

# Добавление товара в корзину
cart_item = cart_service.add_to_cart(user.id, product.id, quantity=2)
print(f"Добавлено в корзину: {cart_item.quantity} шт.")
```

### Получение содержимого корзины
```python
cart_items = cart_service.get_cart_items(user.id)
for item in cart_items:
    print(f"Товар: {item.product.name}, Количество: {item.quantity}")
```

### Обновление количества товара в корзине
```python
updated_item = cart_service.update_cart_item_quantity(cart_item.id, 5)
print(f"Обновлено количество: {updated_item.quantity}")
```

### Удаление товара из корзины
```python
success = cart_service.remove_from_cart(cart_item.id)
if success:
    print("Товар удален из корзины")
```

### Получение общей суммы корзины
```python
total_items, total_amount = cart_service.get_cart_total(user.id)
print(f"В корзине {total_items} товаров на сумму {total_amount} ₽")
```

### Очистка корзины
```python
success = cart_service.clear_cart(user.id)
if success:
    print("Корзина очищена")
```

## Работа с заказами

### Создание заказа
```python
order_service = OrderService(db)

order_data = OrderCreate(
    delivery_method=DeliveryMethod.COURIER,
    delivery_address="ул. Пушкина, д. 1, кв. 1",
    customer_name="John Doe",
    customer_phone="+7(999)123-45-67",
    notes="Позвонить перед доставкой"
)
order = order_service.create_order(user.id, order_data)
print(f"Создан заказ: {order.order_number}")
```

### Получение заказов пользователя
```python
orders = order_service.get_user_orders(user.id)
for order in orders:
    print(f"Заказ: {order.order_number}, Статус: {order.status}")
```

### Поиск заказа по номеру
```python
order = order_service.get_order_by_number("ORD-20231201-1234")
if order:
    print(f"Найден заказ: {order.order_number}")
```

### Обновление статуса заказа
```python
from models import OrderStatus

updated_order = order_service.update_order_status(order.id, OrderStatus.CONFIRMED)
print(f"Статус заказа обновлен: {updated_order.status}")
```

### Получение всех заказов (для администратора)
```python
all_orders = order_service.get_all_orders()
for order in all_orders:
    print(f"Заказ: {order.order_number}, Клиент: {order.customer_name}")
```

## Комплексные примеры

### Полный цикл покупки
```python
def complete_purchase_flow():
    """Пример полного цикла покупки"""
    db = get_db_session()
    
    try:
        # Создание сервисов
        user_service = UserService(db)
        product_service = ProductService(db)
        cart_service = CartService(db)
        order_service = OrderService(db)
        
        # 1. Получение или создание пользователя
        user = user_service.get_or_create_user(
            telegram_id=12345,
            username="customer",
            first_name="Customer",
            last_name="Name"
        )
        
        # 2. Поиск товара
        product = product_service.get_product_by_id(1)
        if not product:
            print("Товар не найден")
            return
        
        # 3. Добавление в корзину
        cart_item = cart_service.add_to_cart(user.id, product.id, 2)
        print(f"Добавлено в корзину: {product.name} x{cart_item.quantity}")
        
        # 4. Проверка корзины
        total_items, total_amount = cart_service.get_cart_total(user.id)
        print(f"В корзине: {total_items} товаров на сумму {total_amount} ₽")
        
        # 5. Создание заказа
        order_data = OrderCreate(
            delivery_method=DeliveryMethod.COURIER,
            delivery_address="ул. Примерная, д. 1",
            customer_name="Customer Name",
            customer_phone="+7(999)123-45-67"
        )
        order = order_service.create_order(user.id, order_data)
        print(f"Заказ создан: {order.order_number}")
        
        # 6. Подтверждение заказа
        confirmed_order = order_service.update_order_status(order.id, OrderStatus.CONFIRMED)
        print(f"Заказ подтвержден: {confirmed_order.status}")
        
    finally:
        db.close()

# Запуск примера
complete_purchase_flow()
```

### Административные функции
```python
def admin_functions_example():
    """Пример административных функций"""
    db = get_db_session()
    
    try:
        # Создание сервисов
        category_service = CategoryService(db)
        product_service = ProductService(db)
        order_service = OrderService(db)
        
        # 1. Создание новой категории
        category_data = CategoryCreate(
            name="Новая категория",
            description="Описание новой категории"
        )
        category = category_service.create_category(category_data)
        print(f"Создана категория: {category.name}")
        
        # 2. Добавление товара в новую категорию
        product_data = ProductCreate(
            name="Новый товар",
            description="Описание нового товара",
            price=1000.0,
            stock_quantity=5,
            category_id=category.id
        )
        product = product_service.create_product(product_data)
        print(f"Создан товар: {product.name}")
        
        # 3. Просмотр всех заказов
        orders = order_service.get_all_orders()
        print(f"Всего заказов: {len(orders)}")
        
        # 4. Обновление статуса заказа
        if orders:
            order = orders[0]
            updated_order = order_service.update_order_status(
                order.id, OrderStatus.SHIPPED
            )
            print(f"Заказ {order.order_number} отправлен")
        
    finally:
        db.close()

# Запуск примера
admin_functions_example()
```

### Аналитика и отчеты
```python
def analytics_example():
    """Пример аналитических функций"""
    db = get_db_session()
    
    try:
        order_service = OrderService(db)
        product_service = ProductService(db)
        user_service = UserService(db)
        
        # 1. Статистика заказов
        all_orders = order_service.get_all_orders()
        total_orders = len(all_orders)
        total_revenue = sum(order.total_amount for order in all_orders)
        
        print(f"Всего заказов: {total_orders}")
        print(f"Общая выручка: {total_revenue} ₽")
        
        # 2. Статистика по статусам
        status_counts = {}
        for order in all_orders:
            status_counts[order.status] = status_counts.get(order.status, 0) + 1
        
        print("Статистика по статусам:")
        for status, count in status_counts.items():
            print(f"  {status}: {count}")
        
        # 3. Топ товары
        products = product_service.get_all_products()
        print(f"Всего товаров: {len(products)}")
        
        # 4. Количество пользователей
        # Примечание: В реальном приложении добавьте метод get_all_users()
        print("Аналитика завершена")
        
    finally:
        db.close()

# Запуск примера
analytics_example()
```

## Обработка ошибок

### Пример с обработкой ошибок
```python
def safe_product_creation():
    """Безопасное создание товара с обработкой ошибок"""
    db = get_db_session()
    
    try:
        product_service = ProductService(db)
        
        product_data = ProductCreate(
            name="Тестовый товар",
            price=100.0,
            category_id=1
        )
        
        product = product_service.create_product(product_data)
        print(f"Товар создан: {product.name}")
        
    except Exception as e:
        print(f"Ошибка при создании товара: {e}")
        
    finally:
        db.close()

# Запуск примера
safe_product_creation()
```

### Валидация данных
```python
def validate_order_data(order_data: dict) -> bool:
    """Валидация данных заказа"""
    required_fields = ['delivery_method', 'delivery_address', 'customer_name', 'customer_phone']
    
    for field in required_fields:
        if field not in order_data or not order_data[field]:
            print(f"Отсутствует обязательное поле: {field}")
            return False
    
    # Валидация телефона
    from utils import validate_phone
    if not validate_phone(order_data['customer_phone']):
        print("Неверный формат телефона")
        return False
    
    return True

# Пример использования
order_data = {
    'delivery_method': 'courier',
    'delivery_address': 'ул. Пушкина, д. 1',
    'customer_name': 'John Doe',
    'customer_phone': '+7(999)123-45-67'
}

if validate_order_data(order_data):
    print("Данные заказа валидны")
else:
    print("Данные заказа невалидны")
```

## Асинхронные операции

### Пример асинхронной работы
```python
import asyncio
from database import get_db_session

async def async_operations():
    """Пример асинхронных операций"""
    db = get_db_session()
    
    try:
        product_service = ProductService(db)
        
        # Получение товаров асинхронно
        products = product_service.get_all_products()
        
        # Обработка товаров
        for product in products:
            print(f"Обработка товара: {product.name}")
            # Здесь можно добавить асинхронные операции
            await asyncio.sleep(0.1)  # Имитация асинхронной работы
        
    finally:
        db.close()

# Запуск асинхронного примера
# asyncio.run(async_operations())
```

## Интеграция с внешними API

### Пример интеграции с платежной системой
```python
def process_payment(order_id: int, amount: float) -> bool:
    """Обработка платежа (пример)"""
    # Здесь будет интеграция с реальной платежной системой
    print(f"Обработка платежа для заказа {order_id} на сумму {amount} ₽")
    
    # Имитация успешного платежа
    return True

def complete_order_with_payment():
    """Завершение заказа с обработкой платежа"""
    db = get_db_session()
    
    try:
        order_service = OrderService(db)
        
        # Получение заказа
        order = order_service.get_order_by_id(1)
        if not order:
            print("Заказ не найден")
            return
        
        # Обработка платежа
        payment_success = process_payment(order.id, order.total_amount)
        
        if payment_success:
            # Обновление статуса заказа
            order_service.update_order_status(order.id, OrderStatus.CONFIRMED)
            print(f"Заказ {order.order_number} оплачен и подтвержден")
        else:
            print("Ошибка при обработке платежа")
        
    finally:
        db.close()

# Запуск примера
complete_order_with_payment()
```

---

**Примечание:** Все примеры предназначены для демонстрации возможностей API. В реальном приложении добавьте дополнительную обработку ошибок и валидацию данных.
