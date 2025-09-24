"""
Business logic services for the E-commerce Telegram Bot
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional, Tuple
from datetime import datetime
import uuid
import random
import string

from database import Category, Product, User, CartItem, Order, OrderItem
from models import (
    CategoryCreate, CategoryUpdate, ProductCreate, ProductUpdate,
    UserCreate, UserUpdate, CartItemCreate, CartItemUpdate,
    OrderCreate, OrderUpdate, OrderStatus, DeliveryMethod
)


class CategoryService:
    """Service for category operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_categories(self) -> List[Category]:
        """Get all active categories"""
        return self.db.query(Category).filter(Category.is_active == True).all()
    
    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """Get category by ID"""
        return self.db.query(Category).filter(Category.id == category_id).first()
    
    def create_category(self, category_data: CategoryCreate) -> Category:
        """Create new category"""
        category = Category(**category_data.dict())
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category
    
    def update_category(self, category_id: int, category_data: CategoryUpdate) -> Optional[Category]:
        """Update category"""
        category = self.get_category_by_id(category_id)
        if not category:
            return None
        
        update_data = category_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(category, field, value)
        
        self.db.commit()
        self.db.refresh(category)
        return category
    
    def delete_category(self, category_id: int) -> bool:
        """Delete category (soft delete)"""
        category = self.get_category_by_id(category_id)
        if not category:
            return False
        
        category.is_active = False
        self.db.commit()
        return True


class ProductService:
    """Service for product operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_products_by_category(self, category_id: int) -> List[Product]:
        """Get all active products in category"""
        return self.db.query(Product).filter(
            and_(Product.category_id == category_id, Product.is_active == True)
        ).all()
    
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        return self.db.query(Product).filter(Product.id == product_id).first()
    
    def get_all_products(self) -> List[Product]:
        """Get all active products"""
        return self.db.query(Product).filter(Product.is_active == True).all()
    
    def create_product(self, product_data: ProductCreate) -> Product:
        """Create new product"""
        product = Product(**product_data.dict())
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product
    
    def update_product(self, product_id: int, product_data: ProductUpdate) -> Optional[Product]:
        """Update product"""
        product = self.get_product_by_id(product_id)
        if not product:
            return None
        
        update_data = product_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        
        self.db.commit()
        self.db.refresh(product)
        return product
    
    def delete_product(self, product_id: int) -> bool:
        """Delete product (soft delete)"""
        product = self.get_product_by_id(product_id)
        if not product:
            return False
        
        product.is_active = False
        self.db.commit()
        return True


class UserService:
    """Service for user operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Get user by Telegram ID"""
        return self.db.query(User).filter(User.telegram_id == telegram_id).first()
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create new user"""
        user = User(**user_data.dict())
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_or_create_user(self, telegram_id: int, username: str = None, 
                          first_name: str = None, last_name: str = None) -> User:
        """Get existing user or create new one"""
        user = self.get_user_by_telegram_id(telegram_id)
        if not user:
            user_data = UserCreate(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            user = self.create_user(user_data)
        return user
    
    def update_user(self, telegram_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update user"""
        user = self.get_user_by_telegram_id(telegram_id)
        if not user:
            return None
        
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user


class CartService:
    """Service for cart operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_cart_items(self, user_id: int) -> List[CartItem]:
        """Get all cart items for user"""
        return self.db.query(CartItem).filter(CartItem.user_id == user_id).all()
    
    def add_to_cart(self, user_id: int, product_id: int, quantity: int = 1) -> CartItem:
        """Add product to cart"""
        # Check if item already exists in cart
        existing_item = self.db.query(CartItem).filter(
            and_(CartItem.user_id == user_id, CartItem.product_id == product_id)
        ).first()
        
        if existing_item:
            existing_item.quantity += quantity
            self.db.commit()
            self.db.refresh(existing_item)
            return existing_item
        else:
            cart_item = CartItem(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity
            )
            self.db.add(cart_item)
            self.db.commit()
            self.db.refresh(cart_item)
            return cart_item
    
    def update_cart_item_quantity(self, cart_item_id: int, quantity: int) -> Optional[CartItem]:
        """Update cart item quantity"""
        cart_item = self.db.query(CartItem).filter(CartItem.id == cart_item_id).first()
        if not cart_item:
            return None
        
        cart_item.quantity = quantity
        self.db.commit()
        self.db.refresh(cart_item)
        return cart_item
    
    def remove_from_cart(self, cart_item_id: int) -> bool:
        """Remove item from cart"""
        cart_item = self.db.query(CartItem).filter(CartItem.id == cart_item_id).first()
        if not cart_item:
            return False
        
        self.db.delete(cart_item)
        self.db.commit()
        return True
    
    def clear_cart(self, user_id: int) -> bool:
        """Clear user's cart"""
        self.db.query(CartItem).filter(CartItem.user_id == user_id).delete()
        self.db.commit()
        return True
    
    def get_cart_total(self, user_id: int) -> Tuple[int, float]:
        """Get cart total items and amount"""
        cart_items = self.get_cart_items(user_id)
        total_items = sum(item.quantity for item in cart_items)
        total_amount = sum(item.quantity * item.product.price for item in cart_items)
        return total_items, total_amount


class OrderService:
    """Service for order operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def generate_order_number(self) -> str:
        """Generate unique order number"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"ORD-{timestamp}-{random_suffix}"
    
    def create_order(self, user_id: int, order_data: OrderCreate) -> Order:
        """Create new order from cart"""
        # Get cart items
        cart_items = self.db.query(CartItem).filter(CartItem.user_id == user_id).all()
        if not cart_items:
            raise ValueError("Cart is empty")
        
        # Calculate total amount
        total_amount = sum(item.quantity * item.product.price for item in cart_items)
        
        # Create order
        order = Order(
            order_number=self.generate_order_number(),
            user_id=user_id,
            total_amount=total_amount,
            delivery_method=order_data.delivery_method.value,
            delivery_address=order_data.delivery_address,
            customer_name=order_data.customer_name,
            customer_phone=order_data.customer_phone,
            notes=order_data.notes,
            status=OrderStatus.PENDING.value
        )
        self.db.add(order)
        self.db.flush()  # Get order ID
        
        # Create order items
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            self.db.add(order_item)
        
        # Clear cart
        self.db.query(CartItem).filter(CartItem.user_id == user_id).delete()
        
        self.db.commit()
        self.db.refresh(order)
        return order
    
    def get_user_orders(self, user_id: int) -> List[Order]:
        """Get all orders for user"""
        return self.db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).all()
    
    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        """Get order by ID"""
        return self.db.query(Order).filter(Order.id == order_id).first()
    
    def get_order_by_number(self, order_number: str) -> Optional[Order]:
        """Get order by order number"""
        return self.db.query(Order).filter(Order.order_number == order_number).first()
    
    def update_order_status(self, order_id: int, status: OrderStatus) -> Optional[Order]:
        """Update order status"""
        order = self.get_order_by_id(order_id)
        if not order:
            return None
        
        order.status = status.value
        order.updated_at = datetime.now()
        self.db.commit()
        self.db.refresh(order)
        return order
    
    def get_all_orders(self) -> List[Order]:
        """Get all orders (admin function)"""
        return self.db.query(Order).order_by(Order.created_at.desc()).all()
