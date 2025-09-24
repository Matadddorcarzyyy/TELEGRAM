"""
Inline keyboards for the E-commerce Telegram Bot
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import List, Optional
from database import Category, Product, CartItem, Order
from models import OrderStatus


class KeyboardBuilder:
    """Builder class for creating inline keyboards"""
    
    @staticmethod
    def categories_keyboard(categories: List[Category]) -> InlineKeyboardMarkup:
        """Create keyboard for categories"""
        keyboard = []
        for category in categories:
            keyboard.append([
                InlineKeyboardButton(
                    f"📁 {category.name}",
                    callback_data=f"category_{category.id}"
                )
            ])
        
        # Add main menu button
        keyboard.append([
            InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
        ])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def products_keyboard(products: List[Product], category_id: int) -> InlineKeyboardMarkup:
        """Create keyboard for products in category"""
        keyboard = []
        
        # Add products in rows of 2
        for i in range(0, len(products), 2):
            row = []
            for j in range(2):
                if i + j < len(products):
                    product = products[i + j]
                    row.append(
                        InlineKeyboardButton(
                            f"🛍️ {product.name[:15]}...",
                            callback_data=f"product_{product.id}"
                        )
                    )
            keyboard.append(row)
        
        # Add navigation buttons
        keyboard.append([
            InlineKeyboardButton("⬅️ Назад к категориям", callback_data="categories"),
            InlineKeyboardButton("🛒 Корзина", callback_data="cart")
        ])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def product_detail_keyboard(product: Product) -> InlineKeyboardMarkup:
        """Create keyboard for product detail view"""
        keyboard = [
            [
                InlineKeyboardButton("➕ Добавить в корзину", callback_data=f"add_to_cart_{product.id}"),
                InlineKeyboardButton("🛒 Корзина", callback_data="cart")
            ],
            [
                InlineKeyboardButton("⬅️ Назад", callback_data=f"category_{product.category_id}"),
                InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
            ]
        ]
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def cart_keyboard(cart_items: List[CartItem]) -> InlineKeyboardMarkup:
        """Create keyboard for cart view"""
        keyboard = []
        
        # Add cart items
        for item in cart_items:
            keyboard.append([
                InlineKeyboardButton(
                    f"➖ {item.product.name[:20]}...",
                    callback_data=f"decrease_cart_{item.id}"
                ),
                InlineKeyboardButton(
                    f"❌ Удалить",
                    callback_data=f"remove_cart_{item.id}"
                )
            ])
            keyboard.append([
                InlineKeyboardButton(
                    f"Количество: {item.quantity}",
                    callback_data=f"cart_item_{item.id}"
                )
            ])
        
        # Add action buttons
        if cart_items:
            keyboard.append([
                InlineKeyboardButton("✅ Оформить заказ", callback_data="checkout"),
                InlineKeyboardButton("🗑️ Очистить корзину", callback_data="clear_cart")
            ])
        
        keyboard.append([
            InlineKeyboardButton("⬅️ Назад к товарам", callback_data="categories"),
            InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
        ])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def delivery_method_keyboard() -> InlineKeyboardMarkup:
        """Create keyboard for delivery method selection"""
        keyboard = [
            [
                InlineKeyboardButton("🚚 Курьером", callback_data="delivery_courier"),
                InlineKeyboardButton("📮 Почтой", callback_data="delivery_post")
            ],
            [
                InlineKeyboardButton("🏪 Самовывоз", callback_data="delivery_pickup")
            ],
            [
                InlineKeyboardButton("⬅️ Назад", callback_data="cart")
            ]
        ]
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def order_confirmation_keyboard(order_id: int) -> InlineKeyboardMarkup:
        """Create keyboard for order confirmation"""
        keyboard = [
            [
                InlineKeyboardButton("✅ Подтвердить заказ", callback_data=f"confirm_order_{order_id}"),
                InlineKeyboardButton("❌ Отменить", callback_data="cancel_order")
            ]
        ]
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def main_menu_keyboard() -> InlineKeyboardMarkup:
        """Create main menu keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("🛍️ Каталог товаров", callback_data="categories"),
                InlineKeyboardButton("🛒 Корзина", callback_data="cart")
            ],
            [
                InlineKeyboardButton("📋 Мои заказы", callback_data="my_orders"),
                InlineKeyboardButton("ℹ️ О магазине", callback_data="about")
            ]
        ]
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def admin_keyboard() -> InlineKeyboardMarkup:
        """Create admin keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("📦 Управление товарами", callback_data="admin_products"),
                InlineKeyboardButton("📁 Управление категориями", callback_data="admin_categories")
            ],
            [
                InlineKeyboardButton("📋 Заказы", callback_data="admin_orders"),
                InlineKeyboardButton("👥 Пользователи", callback_data="admin_users")
            ],
            [
                InlineKeyboardButton("📊 Статистика", callback_data="admin_stats"),
                InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
            ]
        ]
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def admin_products_keyboard() -> InlineKeyboardMarkup:
        """Create admin products management keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("➕ Добавить товар", callback_data="admin_add_product"),
                InlineKeyboardButton("✏️ Редактировать товар", callback_data="admin_edit_product")
            ],
            [
                InlineKeyboardButton("📋 Список товаров", callback_data="admin_list_products"),
                InlineKeyboardButton("⬅️ Назад", callback_data="admin_menu")
            ]
        ]
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def admin_categories_keyboard() -> InlineKeyboardMarkup:
        """Create admin categories management keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("➕ Добавить категорию", callback_data="admin_add_category"),
                InlineKeyboardButton("✏️ Редактировать категорию", callback_data="admin_edit_category")
            ],
            [
                InlineKeyboardButton("📋 Список категорий", callback_data="admin_list_categories"),
                InlineKeyboardButton("⬅️ Назад", callback_data="admin_menu")
            ]
        ]
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def admin_orders_keyboard() -> InlineKeyboardMarkup:
        """Create admin orders management keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("📋 Все заказы", callback_data="admin_all_orders"),
                InlineKeyboardButton("⏳ Ожидающие", callback_data="admin_pending_orders")
            ],
            [
                InlineKeyboardButton("🚚 В доставке", callback_data="admin_shipped_orders"),
                InlineKeyboardButton("✅ Завершенные", callback_data="admin_delivered_orders")
            ],
            [
                InlineKeyboardButton("⬅️ Назад", callback_data="admin_menu")
            ]
        ]
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def order_status_keyboard(order_id: int) -> InlineKeyboardMarkup:
        """Create keyboard for order status management"""
        keyboard = [
            [
                InlineKeyboardButton("✅ Подтвердить", callback_data=f"admin_confirm_{order_id}"),
                InlineKeyboardButton("🚚 Отправить", callback_data=f"admin_ship_{order_id}")
            ],
            [
                InlineKeyboardButton("📦 Доставлен", callback_data=f"admin_deliver_{order_id}"),
                InlineKeyboardButton("❌ Отменить", callback_data=f"admin_cancel_{order_id}")
            ],
            [
                InlineKeyboardButton("⬅️ Назад к заказам", callback_data="admin_orders")
            ]
        ]
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def pagination_keyboard(current_page: int, total_pages: int, 
                          callback_prefix: str, **kwargs) -> InlineKeyboardMarkup:
        """Create pagination keyboard"""
        keyboard = []
        
        # Previous and Next buttons
        nav_buttons = []
        if current_page > 1:
            nav_buttons.append(
                InlineKeyboardButton("⬅️", callback_data=f"{callback_prefix}_page_{current_page - 1}")
            )
        
        nav_buttons.append(
            InlineKeyboardButton(f"{current_page}/{total_pages}", callback_data="noop")
        )
        
        if current_page < total_pages:
            nav_buttons.append(
                InlineKeyboardButton("➡️", callback_data=f"{callback_prefix}_page_{current_page + 1}")
            )
        
        if nav_buttons:
            keyboard.append(nav_buttons)
        
        return InlineKeyboardMarkup(keyboard)
