"""
Pydantic models for data validation and serialization
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    """Order status enumeration"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class DeliveryMethod(str, Enum):
    """Delivery method enumeration"""
    PICKUP = "pickup"
    COURIER = "courier"
    POST = "post"


# Category models
class CategoryBase(BaseModel):
    """Base category model"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    is_active: bool = True


class CategoryCreate(CategoryBase):
    """Category creation model"""
    pass


class CategoryUpdate(BaseModel):
    """Category update model"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    is_active: Optional[bool] = None


class CategoryResponse(CategoryBase):
    """Category response model"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Product models
class ProductBase(BaseModel):
    """Base product model"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    photo_url: Optional[str] = None
    stock_quantity: int = Field(default=0, ge=0)
    is_active: bool = True
    category_id: int


class ProductCreate(ProductBase):
    """Product creation model"""
    pass


class ProductUpdate(BaseModel):
    """Product update model"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    photo_url: Optional[str] = None
    stock_quantity: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None
    category_id: Optional[int] = None


class ProductResponse(ProductBase):
    """Product response model"""
    id: int
    created_at: datetime
    category: Optional[CategoryResponse] = None
    
    class Config:
        from_attributes = True


# User models
class UserBase(BaseModel):
    """Base user model"""
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class UserCreate(UserBase):
    """User creation model"""
    pass


class UserUpdate(BaseModel):
    """User update model"""
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class UserResponse(UserBase):
    """User response model"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Cart models
class CartItemBase(BaseModel):
    """Base cart item model"""
    product_id: int
    quantity: int = Field(..., ge=1)


class CartItemCreate(CartItemBase):
    """Cart item creation model"""
    pass


class CartItemUpdate(BaseModel):
    """Cart item update model"""
    quantity: int = Field(..., ge=1)


class CartItemResponse(CartItemBase):
    """Cart item response model"""
    id: int
    product: ProductResponse
    created_at: datetime
    
    class Config:
        from_attributes = True


# Order models
class OrderBase(BaseModel):
    """Base order model"""
    delivery_method: DeliveryMethod
    delivery_address: str = Field(..., min_length=1)
    customer_name: str = Field(..., min_length=1)
    customer_phone: str = Field(..., min_length=1)
    notes: Optional[str] = None


class OrderCreate(OrderBase):
    """Order creation model"""
    pass


class OrderUpdate(BaseModel):
    """Order update model"""
    status: Optional[OrderStatus] = None
    delivery_method: Optional[DeliveryMethod] = None
    delivery_address: Optional[str] = None
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    notes: Optional[str] = None


class OrderItemResponse(BaseModel):
    """Order item response model"""
    id: int
    product: ProductResponse
    quantity: int
    price: float
    
    class Config:
        from_attributes = True


class OrderResponse(OrderBase):
    """Order response model"""
    id: int
    order_number: str
    user_id: int
    total_amount: float
    status: OrderStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    order_items: List[OrderItemResponse] = []
    
    class Config:
        from_attributes = True


# Cart summary model
class CartSummary(BaseModel):
    """Cart summary model"""
    items: List[CartItemResponse]
    total_items: int
    total_amount: float
