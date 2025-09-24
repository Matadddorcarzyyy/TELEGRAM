# 🧪 Руководство по тестированию

## Обзор тестирования

Проект включает комплексную систему тестирования, покрывающую все основные компоненты и функциональность бота.

## Структура тестов

### Файлы тестов
- **tests.py** - Основной файл с unit тестами
- **run_tests.py** - Скрипт для запуска тестов
- **test.db** - Тестовая база данных (создается автоматически)

### Типы тестов
1. **Unit тесты** - Тестирование отдельных компонентов
2. **Интеграционные тесты** - Тестирование взаимодействия компонентов
3. **Функциональные тесты** - Тестирование полных сценариев

## Запуск тестов

### Быстрый запуск
```bash
python run_tests.py
```

### Запуск с покрытием кода
```bash
python run_tests.py coverage
```

### Запуск конкретного теста
```bash
python run_tests.py test:TestCategoryService
```

### Запуск через pytest напрямую
```bash
pytest tests.py -v
```

## Покрытие тестами

### Тестируемые компоненты

#### 1. CategoryService
- ✅ Создание категории
- ✅ Получение всех категорий
- ✅ Получение категории по ID
- ✅ Обновление категории
- ✅ Удаление категории (мягкое удаление)

#### 2. ProductService
- ✅ Создание товара
- ✅ Получение товаров по категории
- ✅ Получение товара по ID
- ✅ Обновление товара
- ✅ Удаление товара (мягкое удаление)

#### 3. UserService
- ✅ Создание пользователя
- ✅ Получение пользователя по Telegram ID
- ✅ Получение или создание пользователя
- ✅ Обновление данных пользователя

#### 4. CartService
- ✅ Добавление товара в корзину
- ✅ Добавление существующего товара
- ✅ Получение элементов корзины
- ✅ Обновление количества товара
- ✅ Удаление товара из корзины
- ✅ Получение общей суммы корзины

#### 5. OrderService
- ✅ Генерация номера заказа
- ✅ Создание заказа
- ✅ Получение заказов пользователя
- ✅ Обновление статуса заказа

#### 6. Утилиты
- ✅ Форматирование цены
- ✅ Валидация телефона
- ✅ Валидация email
- ✅ Расчет стоимости доставки

#### 7. Интеграционные тесты
- ✅ Полный цикл покупки
- ✅ Взаимодействие всех сервисов
- ✅ Работа с базой данных

## Структура тестов

### Фикстуры
```python
@pytest.fixture
def db_session():
    """Создание тестовой сессии БД"""
    
@pytest.fixture
def sample_category(db_session):
    """Создание тестовой категории"""
    
@pytest.fixture
def sample_product(db_session, sample_category):
    """Создание тестового товара"""
    
@pytest.fixture
def sample_user(db_session):
    """Создание тестового пользователя"""
```

### Тестовые классы
```python
class TestCategoryService:
    """Тесты для CategoryService"""
    
class TestProductService:
    """Тесты для ProductService"""
    
class TestUserService:
    """Тесты для UserService"""
    
class TestCartService:
    """Тесты для CartService"""
    
class TestOrderService:
    """Тесты для OrderService"""
    
class TestUtils:
    """Тесты для утилит"""
    
class TestIntegration:
    """Интеграционные тесты"""
```

## Примеры тестов

### Unit тест
```python
def test_create_category(self, db_session):
    """Тест создания категории"""
    service = CategoryService(db_session)
    category_data = CategoryCreate(
        name="New Category",
        description="New category description"
    )
    
    category = service.create_category(category_data)
    
    assert category.name == "New Category"
    assert category.description == "New category description"
    assert category.is_active is True
    assert category.id is not None
```

### Интеграционный тест
```python
def test_full_order_flow(self, db_session):
    """Тест полного цикла покупки"""
    # Создание сервисов
    category_service = CategoryService(db_session)
    product_service = ProductService(db_session)
    user_service = UserService(db_session)
    cart_service = CartService(db_session)
    order_service = OrderService(db_session)
    
    # Создание данных
    category = category_service.create_category(...)
    product = product_service.create_product(...)
    user = user_service.create_user(...)
    
    # Тестирование потока
    cart_item = cart_service.add_to_cart(user.id, product.id, 2)
    order = order_service.create_order(user.id, order_data)
    
    # Проверки
    assert order.total_amount == 200.0
    assert order.status == "pending"
```

## Настройка тестовой среды

### Переменные окружения
```bash
export DATABASE_URL="sqlite:///./test.db"
export DEBUG="True"
export LOG_LEVEL="WARNING"
```

### Изоляция тестов
- Каждый тест использует отдельную сессию БД
- Тестовая БД создается и удаляется для каждого теста
- Мокирование внешних зависимостей

## Мокирование

### Пример мокирования
```python
@patch('services.requests.get')
def test_external_api_call(self, mock_get):
    """Тест с мокированием внешнего API"""
    mock_get.return_value.json.return_value = {'status': 'success'}
    
    result = service.call_external_api()
    
    assert result['status'] == 'success'
    mock_get.assert_called_once()
```

## Тестирование ошибок

### Тест обработки ошибок
```python
def test_handle_database_error(self, db_session):
    """Тест обработки ошибки БД"""
    service = CategoryService(db_session)
    
    # Попытка создать категорию с невалидными данными
    with pytest.raises(ValueError):
        service.create_category(invalid_data)
```

## Параметризованные тесты

### Пример параметризованного теста
```python
@pytest.mark.parametrize("phone,expected", [
    ("+7(999)123-45-67", True),
    ("8(999)123-45-67", True),
    ("invalid", False),
    ("123", False),
])
def test_validate_phone(self, phone, expected):
    """Тест валидации телефона"""
    result = validate_phone(phone)
    assert result == expected
```

## Тестирование производительности

### Тест производительности
```python
def test_large_dataset_performance(self, db_session):
    """Тест производительности с большим объемом данных"""
    service = ProductService(db_session)
    
    # Создание большого количества товаров
    start_time = time.time()
    for i in range(1000):
        service.create_product(product_data)
    end_time = time.time()
    
    assert (end_time - start_time) < 10.0  # Должно выполняться менее 10 секунд
```

## Отчеты о тестировании

### Генерация отчета
```bash
# HTML отчет
pytest --html=report.html --self-contained-html

# XML отчет для CI/CD
pytest --junitxml=report.xml

# Отчет о покрытии
coverage run -m pytest tests.py
coverage report
coverage html
```

### Интерпретация результатов
- **PASSED** - Тест прошел успешно
- **FAILED** - Тест не прошел
- **SKIPPED** - Тест пропущен
- **ERROR** - Ошибка в тесте

## Непрерывная интеграция

### GitHub Actions
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: python run_tests.py
```

## Лучшие практики

### Написание тестов
1. **Один тест - одна проверка**
2. **Понятные имена** тестов и переменных
3. **Изоляция тестов** друг от друга
4. **Использование фикстур** для подготовки данных
5. **Проверка как успешных, так и ошибочных сценариев**

### Организация тестов
1. **Группировка** по функциональности
2. **Использование классов** для группировки связанных тестов
3. **Параметризация** для тестирования множественных случаев
4. **Мокирование** внешних зависимостей

### Поддержка тестов
1. **Регулярный запуск** тестов
2. **Обновление тестов** при изменении кода
3. **Мониторинг покрытия** кода
4. **Анализ результатов** тестирования

## Отладка тестов

### Полезные команды
```bash
# Запуск с подробным выводом
pytest -v -s

# Запуск конкретного теста с отладкой
pytest tests.py::TestCategoryService::test_create_category -v -s

# Запуск с остановкой на первой ошибке
pytest -x

# Запуск только упавших тестов
pytest --lf
```

### Отладочная информация
```python
def test_with_debug_info(self, db_session):
    """Тест с отладочной информацией"""
    service = CategoryService(db_session)
    
    # Добавление отладочной информации
    print(f"Database session: {db_session}")
    print(f"Service: {service}")
    
    result = service.create_category(category_data)
    
    # Проверка с подробной информацией
    assert result is not None, f"Result is None: {result}"
    assert result.name == "Test", f"Expected 'Test', got '{result.name}'"
```

## Метрики качества

### Целевые показатели
- **Покрытие кода**: > 80%
- **Прохождение тестов**: 100%
- **Время выполнения**: < 30 секунд
- **Количество тестов**: > 25

### Мониторинг
- Регулярный запуск тестов
- Отслеживание покрытия кода
- Анализ времени выполнения
- Мониторинг стабильности

---

**Следуйте этим рекомендациям для обеспечения высокого качества и надежности вашего кода!**
