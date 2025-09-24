"""
Unit tests for the E-commerce Telegram Bot
"""
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from database import Base, Category, Product, User, CartItem, Order, OrderItem
from services import CategoryService, ProductService, UserService, CartService, OrderService
from models import CategoryCreate, ProductCreate, UserCreate, OrderCreate, DeliveryMethod, OrderStatus
from utils import format_price, validate_phone, validate_email, calculate_delivery_cost


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    """Create test database session"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_category(db_session):
    """Create sample category for testing"""
    category = Category(
        name="Test Category",
        description="Test category description",
        is_active=True
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


@pytest.fixture
def sample_product(db_session, sample_category):
    """Create sample product for testing"""
    product = Product(
        name="Test Product",
        description="Test product description",
        price=100.0,
        stock_quantity=10,
        is_active=True,
        category_id=sample_category.id
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product


@pytest.fixture
def sample_user(db_session):
    """Create sample user for testing"""
    user = User(
        telegram_id=12345,
        username="testuser",
        first_name="Test",
        last_name="User"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


class TestCategoryService:
    """Test CategoryService"""
    
    def test_create_category(self, db_session):
        """Test category creation"""
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
    
    def test_get_all_categories(self, db_session, sample_category):
        """Test getting all categories"""
        service = CategoryService(db_session)
        categories = service.get_all_categories()
        
        assert len(categories) == 1
        assert categories[0].name == "Test Category"
    
    def test_get_category_by_id(self, db_session, sample_category):
        """Test getting category by ID"""
        service = CategoryService(db_session)
        category = service.get_category_by_id(sample_category.id)
        
        assert category is not None
        assert category.name == "Test Category"
    
    def test_update_category(self, db_session, sample_category):
        """Test category update"""
        service = CategoryService(db_session)
        update_data = CategoryCreate(name="Updated Category")
        
        updated_category = service.update_category(sample_category.id, update_data)
        
        assert updated_category is not None
        assert updated_category.name == "Updated Category"
    
    def test_delete_category(self, db_session, sample_category):
        """Test category deletion (soft delete)"""
        service = CategoryService(db_session)
        
        result = service.delete_category(sample_category.id)
        
        assert result is True
        
        # Check that category is marked as inactive
        category = service.get_category_by_id(sample_category.id)
        assert category.is_active is False


class TestProductService:
    """Test ProductService"""
    
    def test_create_product(self, db_session, sample_category):
        """Test product creation"""
        service = ProductService(db_session)
        product_data = ProductCreate(
            name="New Product",
            description="New product description",
            price=50.0,
            stock_quantity=5,
            category_id=sample_category.id
        )
        
        product = service.create_product(product_data)
        
        assert product.name == "New Product"
        assert product.price == 50.0
        assert product.stock_quantity == 5
        assert product.category_id == sample_category.id
    
    def test_get_products_by_category(self, db_session, sample_category, sample_product):
        """Test getting products by category"""
        service = ProductService(db_session)
        products = service.get_products_by_category(sample_category.id)
        
        assert len(products) == 1
        assert products[0].name == "Test Product"
    
    def test_get_product_by_id(self, db_session, sample_product):
        """Test getting product by ID"""
        service = ProductService(db_session)
        product = service.get_product_by_id(sample_product.id)
        
        assert product is not None
        assert product.name == "Test Product"
    
    def test_update_product(self, db_session, sample_product):
        """Test product update"""
        service = ProductService(db_session)
        update_data = ProductCreate(
            name="Updated Product",
            price=150.0,
            category_id=sample_product.category_id
        )
        
        updated_product = service.update_product(sample_product.id, update_data)
        
        assert updated_product is not None
        assert updated_product.name == "Updated Product"
        assert updated_product.price == 150.0


class TestUserService:
    """Test UserService"""
    
    def test_create_user(self, db_session):
        """Test user creation"""
        service = UserService(db_session)
        user_data = UserCreate(
            telegram_id=54321,
            username="newuser",
            first_name="New",
            last_name="User"
        )
        
        user = service.create_user(user_data)
        
        assert user.telegram_id == 54321
        assert user.username == "newuser"
        assert user.first_name == "New"
    
    def test_get_user_by_telegram_id(self, db_session, sample_user):
        """Test getting user by Telegram ID"""
        service = UserService(db_session)
        user = service.get_user_by_telegram_id(sample_user.telegram_id)
        
        assert user is not None
        assert user.username == "testuser"
    
    def test_get_or_create_user_existing(self, db_session, sample_user):
        """Test get or create user with existing user"""
        service = UserService(db_session)
        user = service.get_or_create_user(
            telegram_id=sample_user.telegram_id,
            username="updated_username"
        )
        
        assert user.id == sample_user.id
        assert user.telegram_id == sample_user.telegram_id
    
    def test_get_or_create_user_new(self, db_session):
        """Test get or create user with new user"""
        service = UserService(db_session)
        user = service.get_or_create_user(
            telegram_id=99999,
            username="newuser",
            first_name="New",
            last_name="User"
        )
        
        assert user.telegram_id == 99999
        assert user.username == "newuser"
        assert user.first_name == "New"


class TestCartService:
    """Test CartService"""
    
    def test_add_to_cart(self, db_session, sample_user, sample_product):
        """Test adding product to cart"""
        service = CartService(db_session)
        
        cart_item = service.add_to_cart(sample_user.id, sample_product.id, 2)
        
        assert cart_item.user_id == sample_user.id
        assert cart_item.product_id == sample_product.id
        assert cart_item.quantity == 2
    
    def test_add_to_cart_existing_item(self, db_session, sample_user, sample_product):
        """Test adding existing item to cart"""
        service = CartService(db_session)
        
        # Add item first time
        service.add_to_cart(sample_user.id, sample_product.id, 2)
        
        # Add same item again
        cart_item = service.add_to_cart(sample_user.id, sample_product.id, 3)
        
        assert cart_item.quantity == 5  # 2 + 3
    
    def test_get_cart_items(self, db_session, sample_user, sample_product):
        """Test getting cart items"""
        service = CartService(db_session)
        
        # Add item to cart
        service.add_to_cart(sample_user.id, sample_product.id, 2)
        
        cart_items = service.get_cart_items(sample_user.id)
        
        assert len(cart_items) == 1
        assert cart_items[0].quantity == 2
    
    def test_update_cart_item_quantity(self, db_session, sample_user, sample_product):
        """Test updating cart item quantity"""
        service = CartService(db_session)
        
        # Add item to cart
        cart_item = service.add_to_cart(sample_user.id, sample_product.id, 2)
        
        # Update quantity
        updated_item = service.update_cart_item_quantity(cart_item.id, 5)
        
        assert updated_item.quantity == 5
    
    def test_remove_from_cart(self, db_session, sample_user, sample_product):
        """Test removing item from cart"""
        service = CartService(db_session)
        
        # Add item to cart
        cart_item = service.add_to_cart(sample_user.id, sample_product.id, 2)
        
        # Remove item
        result = service.remove_from_cart(cart_item.id)
        
        assert result is True
        
        # Check that item is removed
        cart_items = service.get_cart_items(sample_user.id)
        assert len(cart_items) == 0
    
    def test_get_cart_total(self, db_session, sample_user, sample_product):
        """Test getting cart total"""
        service = CartService(db_session)
        
        # Add item to cart
        service.add_to_cart(sample_user.id, sample_product.id, 3)
        
        total_items, total_amount = service.get_cart_total(sample_user.id)
        
        assert total_items == 3
        assert total_amount == 300.0  # 3 * 100.0


class TestOrderService:
    """Test OrderService"""
    
    def test_generate_order_number(self, db_session):
        """Test order number generation"""
        service = OrderService(db_session)
        
        order_number = service.generate_order_number()
        
        assert order_number.startswith("ORD-")
        assert len(order_number) > 10
    
    def test_create_order(self, db_session, sample_user, sample_product):
        """Test order creation"""
        service = OrderService(db_session)
        cart_service = CartService(db_session)
        
        # Add item to cart
        cart_service.add_to_cart(sample_user.id, sample_product.id, 2)
        
        # Create order
        order_data = OrderCreate(
            delivery_method=DeliveryMethod.COURIER,
            delivery_address="Test Address",
            customer_name="Test Customer",
            customer_phone="+7(999)123-45-67"
        )
        
        order = service.create_order(sample_user.id, order_data)
        
        assert order.user_id == sample_user.id
        assert order.total_amount == 200.0  # 2 * 100.0
        assert order.delivery_method == "courier"
        assert order.customer_name == "Test Customer"
        assert order.status == "pending"
        
        # Check that cart is cleared
        cart_items = cart_service.get_cart_items(sample_user.id)
        assert len(cart_items) == 0
    
    def test_get_user_orders(self, db_session, sample_user, sample_product):
        """Test getting user orders"""
        service = OrderService(db_session)
        cart_service = CartService(db_session)
        
        # Add item to cart and create order
        cart_service.add_to_cart(sample_user.id, sample_product.id, 1)
        order_data = OrderCreate(
            delivery_method=DeliveryMethod.PICKUP,
            delivery_address="Test Address",
            customer_name="Test Customer",
            customer_phone="+7(999)123-45-67"
        )
        order = service.create_order(sample_user.id, order_data)
        
        # Get user orders
        orders = service.get_user_orders(sample_user.id)
        
        assert len(orders) == 1
        assert orders[0].id == order.id
    
    def test_update_order_status(self, db_session, sample_user, sample_product):
        """Test updating order status"""
        service = OrderService(db_session)
        cart_service = CartService(db_session)
        
        # Create order
        cart_service.add_to_cart(sample_user.id, sample_product.id, 1)
        order_data = OrderCreate(
            delivery_method=DeliveryMethod.PICKUP,
            delivery_address="Test Address",
            customer_name="Test Customer",
            customer_phone="+7(999)123-45-67"
        )
        order = service.create_order(sample_user.id, order_data)
        
        # Update status
        updated_order = service.update_order_status(order.id, OrderStatus.CONFIRMED)
        
        assert updated_order.status == "confirmed"


class TestUtils:
    """Test utility functions"""
    
    def test_format_price(self):
        """Test price formatting"""
        assert format_price(123.45) == "123.45 ₽"
        assert format_price(0) == "0.00 ₽"
        assert format_price(1000) == "1000.00 ₽"
    
    def test_validate_phone(self):
        """Test phone validation"""
        assert validate_phone("+7(999)123-45-67") is True
        assert validate_phone("8(999)123-45-67") is True
        assert validate_phone("+7 999 123 45 67") is True
        assert validate_phone("invalid") is False
        assert validate_phone("123") is False
    
    def test_validate_email(self):
        """Test email validation"""
        assert validate_email("test@example.com") is True
        assert validate_email("user.name@domain.co.uk") is True
        assert validate_email("invalid-email") is False
        assert validate_email("@domain.com") is False
        assert validate_email("user@") is False
    
    def test_calculate_delivery_cost(self):
        """Test delivery cost calculation"""
        assert calculate_delivery_cost("pickup", 1000) == 0.0
        assert calculate_delivery_cost("courier", 1000) == 300.0
        assert calculate_delivery_cost("courier", 3000) == 0.0
        assert calculate_delivery_cost("post", 1000) == 200.0
        assert calculate_delivery_cost("post", 2000) == 0.0


class TestIntegration:
    """Integration tests"""
    
    def test_full_order_flow(self, db_session):
        """Test complete order flow"""
        # Create services
        category_service = CategoryService(db_session)
        product_service = ProductService(db_session)
        user_service = UserService(db_session)
        cart_service = CartService(db_session)
        order_service = OrderService(db_session)
        
        # Create category
        category_data = CategoryCreate(name="Test Category")
        category = category_service.create_category(category_data)
        
        # Create product
        product_data = ProductCreate(
            name="Test Product",
            price=50.0,
            stock_quantity=10,
            category_id=category.id
        )
        product = product_service.create_product(product_data)
        
        # Create user
        user_data = UserCreate(telegram_id=12345, username="testuser")
        user = user_service.create_user(user_data)
        
        # Add to cart
        cart_item = cart_service.add_to_cart(user.id, product.id, 2)
        assert cart_item.quantity == 2
        
        # Check cart total
        total_items, total_amount = cart_service.get_cart_total(user.id)
        assert total_items == 2
        assert total_amount == 100.0
        
        # Create order
        order_data = OrderCreate(
            delivery_method=DeliveryMethod.COURIER,
            delivery_address="Test Address",
            customer_name="Test Customer",
            customer_phone="+7(999)123-45-67"
        )
        order = order_service.create_order(user.id, order_data)
        
        # Verify order
        assert order.total_amount == 100.0
        assert order.status == "pending"
        assert len(order.order_items) == 1
        assert order.order_items[0].quantity == 2
        
        # Verify cart is cleared
        cart_items = cart_service.get_cart_items(user.id)
        assert len(cart_items) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
