"""
Message and callback handlers for the E-commerce Telegram Bot
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from sqlalchemy.orm import Session
from typing import Dict, Any
import logging

from database import get_db_session
from services import CategoryService, ProductService, UserService, CartService, OrderService
from keyboards import KeyboardBuilder
from models import OrderCreate, DeliveryMethod, OrderStatus
from config import settings

logger = logging.getLogger(__name__)


class BotHandlers:
    """Main handlers class for the bot"""
    
    def __init__(self):
        self.user_states: Dict[int, Dict[str, Any]] = {}
    
    def get_user_state(self, user_id: int) -> Dict[str, Any]:
        """Get user state"""
        if user_id not in self.user_states:
            self.user_states[user_id] = {}
        return self.user_states[user_id]
    
    def set_user_state(self, user_id: int, state: str, data: Any = None):
        """Set user state"""
        user_state = self.get_user_state(user_id)
        user_state['state'] = state
        if data:
            user_state['data'] = data
    
    def clear_user_state(self, user_id: int):
        """Clear user state"""
        if user_id in self.user_states:
            del self.user_states[user_id]
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        db = get_db_session()
        
        try:
            # Get or create user
            user_service = UserService(db)
            db_user = user_service.get_or_create_user(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
            
            # Clear any existing state
            self.clear_user_state(user.id)
            
            # Send welcome message
            keyboard = KeyboardBuilder.main_menu_keyboard()
            await update.message.reply_text(
                settings.welcome_message,
                reply_markup=keyboard
            )
            
        except Exception as e:
            logger.error(f"Error in start command: {e}")
            await update.message.reply_text("Произошла ошибка. Попробуйте позже.")
        finally:
            db.close()
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🛍️ *Интернет-магазин - Помощь*

*Основные команды:*
/start - Начать работу с ботом
/help - Показать эту справку
/cart - Показать корзину
/orders - Мои заказы

*Как пользоваться:*
1. Выберите категорию товаров
2. Просмотрите товары в категории
3. Добавьте понравившиеся товары в корзину
4. Оформите заказ

*Для администраторов:*
/admin - Панель администратора
        """
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
    
    async def admin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /admin command"""
        user = update.effective_user
        
        if user.id != settings.admin_user_id:
            await update.message.reply_text("У вас нет прав администратора.")
            return
        
        keyboard = KeyboardBuilder.admin_keyboard()
        await update.message.reply_text(
            "🔧 *Панель администратора*",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def callback_query_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle callback queries"""
        query = update.callback_query
        await query.answer()
        
        user = update.effective_user
        data = query.data
        
        db = get_db_session()
        
        try:
            if data == "main_menu":
                await self.show_main_menu(query, user)
            elif data == "categories":
                await self.show_categories(query, db)
            elif data.startswith("category_"):
                category_id = int(data.split("_")[1])
                await self.show_products(query, db, category_id)
            elif data.startswith("product_"):
                product_id = int(data.split("_")[1])
                await self.show_product_detail(query, db, product_id)
            elif data.startswith("add_to_cart_"):
                product_id = int(data.split("_")[3])
                await self.add_to_cart(query, db, user, product_id)
            elif data == "cart":
                await self.show_cart(query, db, user)
            elif data.startswith("decrease_cart_"):
                cart_item_id = int(data.split("_")[2])
                await self.decrease_cart_item(query, db, cart_item_id)
            elif data.startswith("remove_cart_"):
                cart_item_id = int(data.split("_")[2])
                await self.remove_cart_item(query, db, cart_item_id)
            elif data == "checkout":
                await self.start_checkout(query, db, user)
            elif data.startswith("delivery_"):
                delivery_method = data.split("_")[1]
                await self.select_delivery_method(query, user, delivery_method)
            elif data.startswith("confirm_order_"):
                order_id = int(data.split("_")[2])
                await self.confirm_order(query, db, order_id)
            elif data == "my_orders":
                await self.show_user_orders(query, db, user)
            elif data == "about":
                await self.show_about(query)
            elif data == "admin_menu":
                await self.show_admin_menu(query, user)
            elif data == "admin_products":
                await self.show_admin_products(query)
            elif data == "admin_categories":
                await self.show_admin_categories(query)
            elif data == "admin_orders":
                await self.show_admin_orders(query, db)
            elif data == "admin_all_orders":
                await self.show_all_orders(query, db)
            elif data.startswith("admin_confirm_"):
                order_id = int(data.split("_")[2])
                await self.admin_confirm_order(query, db, order_id)
            elif data.startswith("admin_ship_"):
                order_id = int(data.split("_")[2])
                await self.admin_ship_order(query, db, order_id)
            elif data.startswith("admin_deliver_"):
                order_id = int(data.split("_")[2])
                await self.admin_deliver_order(query, db, order_id)
            elif data.startswith("admin_cancel_"):
                order_id = int(data.split("_")[2])
                await self.admin_cancel_order(query, db, order_id)
            else:
                await query.edit_message_text("Неизвестная команда.")
                
        except Exception as e:
            logger.error(f"Error in callback query handler: {e}")
            await query.edit_message_text("Произошла ошибка. Попробуйте позже.")
        finally:
            db.close()
    
    async def show_main_menu(self, query, user):
        """Show main menu"""
        keyboard = KeyboardBuilder.main_menu_keyboard()
        if user.id == settings.admin_user_id:
            keyboard.inline_keyboard.append([
                InlineKeyboardButton("🔧 Админ панель", callback_data="admin_menu")
            ])
        
        await query.edit_message_text(
            settings.welcome_message,
            reply_markup=keyboard
        )
    
    async def show_categories(self, query, db):
        """Show categories"""
        category_service = CategoryService(db)
        categories = category_service.get_all_categories()
        
        if not categories:
            await query.edit_message_text(
                "📁 Категории товаров пока не добавлены.",
                reply_markup=KeyboardBuilder.main_menu_keyboard()
            )
            return
        
        keyboard = KeyboardBuilder.categories_keyboard(categories)
        await query.edit_message_text(
            "📁 *Выберите категорию товаров:*",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def show_products(self, query, db, category_id):
        """Show products in category"""
        category_service = CategoryService(db)
        product_service = ProductService(db)
        
        category = category_service.get_category_by_id(category_id)
        if not category:
            await query.edit_message_text("Категория не найдена.")
            return
        
        products = product_service.get_products_by_category(category_id)
        
        if not products:
            await query.edit_message_text(
                f"📦 В категории '{category.name}' пока нет товаров.",
                reply_markup=KeyboardBuilder.main_menu_keyboard()
            )
            return
        
        keyboard = KeyboardBuilder.products_keyboard(products, category_id)
        await query.edit_message_text(
            f"📦 *Товары в категории '{category.name}':*",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def show_product_detail(self, query, db, product_id):
        """Show product detail"""
        product_service = ProductService(db)
        product = product_service.get_product_by_id(product_id)
        
        if not product:
            await query.edit_message_text("Товар не найден.")
            return
        
        # Format product info
        text = f"""
🛍️ *{product.name}*

💰 Цена: {product.price:.2f} ₽
📦 В наличии: {product.stock_quantity} шт.

📝 *Описание:*
{product.description or 'Описание не указано'}
        """
        
        keyboard = KeyboardBuilder.product_detail_keyboard(product)
        
        if product.photo_url:
            await query.edit_message_media(
                media=product.photo_url,
                caption=text,
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await query.edit_message_text(
                text,
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN
            )
    
    async def add_to_cart(self, query, db, user, product_id):
        """Add product to cart"""
        user_service = UserService(db)
        cart_service = CartService(db)
        product_service = ProductService(db)
        
        # Get or create user
        db_user = user_service.get_or_create_user(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        
        # Check product availability
        product = product_service.get_product_by_id(product_id)
        if not product or product.stock_quantity <= 0:
            await query.answer("Товар недоступен", show_alert=True)
            return
        
        # Add to cart
        cart_service.add_to_cart(db_user.id, product_id)
        
        await query.answer(f"✅ {product.name} добавлен в корзину!")
    
    async def show_cart(self, query, db, user):
        """Show cart"""
        user_service = UserService(db)
        cart_service = CartService(db)
        
        # Get user
        db_user = user_service.get_user_by_telegram_id(user.id)
        if not db_user:
            await query.edit_message_text(
                "Сначала начните работу с ботом командой /start",
                reply_markup=KeyboardBuilder.main_menu_keyboard()
            )
            return
        
        cart_items = cart_service.get_cart_items(db_user.id)
        
        if not cart_items:
            await query.edit_message_text(
                settings.cart_empty_message,
                reply_markup=KeyboardBuilder.main_menu_keyboard()
            )
            return
        
        # Format cart content
        text = "🛒 *Ваша корзина:*\n\n"
        total_amount = 0
        
        for item in cart_items:
            item_total = item.quantity * item.product.price
            total_amount += item_total
            text += f"🛍️ {item.product.name}\n"
            text += f"   Количество: {item.quantity}\n"
            text += f"   Цена: {item.product.price:.2f} ₽\n"
            text += f"   Сумма: {item_total:.2f} ₽\n\n"
        
        text += f"💰 *Общая сумма: {total_amount:.2f} ₽*"
        
        keyboard = KeyboardBuilder.cart_keyboard(cart_items)
        await query.edit_message_text(
            text,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def decrease_cart_item(self, query, db, cart_item_id):
        """Decrease cart item quantity"""
        cart_service = CartService(db)
        
        cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
        if not cart_item:
            await query.answer("Товар не найден в корзине", show_alert=True)
            return
        
        if cart_item.quantity > 1:
            cart_service.update_cart_item_quantity(cart_item_id, cart_item.quantity - 1)
            await query.answer("Количество уменьшено")
        else:
            cart_service.remove_from_cart(cart_item_id)
            await query.answer("Товар удален из корзины")
        
        # Refresh cart view
        await self.show_cart(query, db, query.from_user)
    
    async def remove_cart_item(self, query, db, cart_item_id):
        """Remove cart item"""
        cart_service = CartService(db)
        
        success = cart_service.remove_from_cart(cart_item_id)
        if success:
            await query.answer("Товар удален из корзины")
            # Refresh cart view
            await self.show_cart(query, db, query.from_user)
        else:
            await query.answer("Ошибка при удалении товара", show_alert=True)
    
    async def start_checkout(self, query, db, user):
        """Start checkout process"""
        user_service = UserService(db)
        cart_service = CartService(db)
        
        # Get user
        db_user = user_service.get_user_by_telegram_id(user.id)
        if not db_user:
            await query.edit_message_text("Пользователь не найден.")
            return
        
        # Check cart
        cart_items = cart_service.get_cart_items(db_user.id)
        if not cart_items:
            await query.edit_message_text(
                settings.cart_empty_message,
                reply_markup=KeyboardBuilder.main_menu_keyboard()
            )
            return
        
        # Set user state for checkout
        self.set_user_state(user.id, "checkout_delivery")
        
        keyboard = KeyboardBuilder.delivery_method_keyboard()
        await query.edit_message_text(
            "🚚 *Выберите способ доставки:*",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def select_delivery_method(self, query, user, delivery_method):
        """Select delivery method"""
        # Set delivery method in user state
        user_state = self.get_user_state(user.id)
        user_state['delivery_method'] = delivery_method
        self.set_user_state(user.id, "checkout_contact_info")
        
        await query.edit_message_text(
            "📝 *Введите ваши контактные данные:*\n\n"
            "Формат: Имя Фамилия, Телефон, Адрес\n"
            "Пример: Иван Петров, +7(999)123-45-67, ул. Пушкина, д. 1, кв. 1",
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def confirm_order(self, query, db, order_id):
        """Confirm order"""
        order_service = OrderService(db)
        
        order = order_service.get_order_by_id(order_id)
        if not order:
            await query.edit_message_text("Заказ не найден.")
            return
        
        # Update order status to confirmed
        order_service.update_order_status(order_id, OrderStatus.CONFIRMED)
        
        await query.edit_message_text(
            f"✅ *Заказ подтвержден!*\n\n"
            f"📋 Номер заказа: {order.order_number}\n"
            f"💰 Сумма: {order.total_amount:.2f} ₽\n"
            f"🚚 Доставка: {order.delivery_method}\n\n"
            f"Спасибо за покупку!",
            reply_markup=KeyboardBuilder.main_menu_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Clear user state
        self.clear_user_state(query.from_user.id)
    
    async def show_user_orders(self, query, db, user):
        """Show user orders"""
        user_service = UserService(db)
        order_service = OrderService(db)
        
        # Get user
        db_user = user_service.get_user_by_telegram_id(user.id)
        if not db_user:
            await query.edit_message_text("Пользователь не найден.")
            return
        
        orders = order_service.get_user_orders(db_user.id)
        
        if not orders:
            await query.edit_message_text(
                "📋 У вас пока нет заказов.",
                reply_markup=KeyboardBuilder.main_menu_keyboard()
            )
            return
        
        text = "📋 *Ваши заказы:*\n\n"
        
        for order in orders[:5]:  # Show last 5 orders
            status_emoji = {
                "pending": "⏳",
                "confirmed": "✅",
                "shipped": "🚚",
                "delivered": "📦",
                "cancelled": "❌"
            }.get(order.status, "❓")
            
            text += f"{status_emoji} *{order.order_number}*\n"
            text += f"💰 {order.total_amount:.2f} ₽\n"
            text += f"📅 {order.created_at.strftime('%d.%m.%Y %H:%M')}\n"
            text += f"📊 Статус: {order.status}\n\n"
        
        keyboard = KeyboardBuilder.main_menu_keyboard()
        await query.edit_message_text(
            text,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def show_about(self, query):
        """Show about information"""
        text = """
🛍️ *Интернет-магазин*

Добро пожаловать в наш интернет-магазин!

*Наши преимущества:*
✅ Широкий ассортимент товаров
✅ Быстрая доставка
✅ Качественное обслуживание
✅ Конкурентные цены

*Способы доставки:*
🚚 Курьерская доставка
📮 Почтовая доставка
🏪 Самовывоз

*Контакты:*
📞 Телефон: +7(999)123-45-67
📧 Email: info@shop.ru
        """
        
        await query.edit_message_text(
            text,
            reply_markup=KeyboardBuilder.main_menu_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
    
    # Admin handlers
    async def show_admin_menu(self, query, user):
        """Show admin menu"""
        if user.id != settings.admin_user_id:
            await query.edit_message_text("У вас нет прав администратора.")
            return
        
        keyboard = KeyboardBuilder.admin_keyboard()
        await query.edit_message_text(
            "🔧 *Панель администратора*",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def show_admin_products(self, query):
        """Show admin products menu"""
        keyboard = KeyboardBuilder.admin_products_keyboard()
        await query.edit_message_text(
            "📦 *Управление товарами*",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def show_admin_categories(self, query):
        """Show admin categories menu"""
        keyboard = KeyboardBuilder.admin_categories_keyboard()
        await query.edit_message_text(
            "📁 *Управление категориями*",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def show_admin_orders(self, query, db):
        """Show admin orders menu"""
        keyboard = KeyboardBuilder.admin_orders_keyboard()
        await query.edit_message_text(
            "📋 *Управление заказами*",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def show_all_orders(self, query, db):
        """Show all orders"""
        order_service = OrderService(db)
        orders = order_service.get_all_orders()
        
        if not orders:
            await query.edit_message_text(
                "📋 Заказов пока нет.",
                reply_markup=KeyboardBuilder.admin_orders_keyboard()
            )
            return
        
        text = "📋 *Все заказы:*\n\n"
        
        for order in orders[:10]:  # Show last 10 orders
            status_emoji = {
                "pending": "⏳",
                "confirmed": "✅",
                "shipped": "🚚",
                "delivered": "📦",
                "cancelled": "❌"
            }.get(order.status, "❓")
            
            text += f"{status_emoji} *{order.order_number}*\n"
            text += f"👤 {order.customer_name}\n"
            text += f"💰 {order.total_amount:.2f} ₽\n"
            text += f"📅 {order.created_at.strftime('%d.%m.%Y %H:%M')}\n"
            text += f"📊 Статус: {order.status}\n\n"
        
        keyboard = KeyboardBuilder.admin_orders_keyboard()
        await query.edit_message_text(
            text,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def admin_confirm_order(self, query, db, order_id):
        """Admin confirm order"""
        order_service = OrderService(db)
        
        order = order_service.update_order_status(order_id, OrderStatus.CONFIRMED)
        if order:
            await query.answer("Заказ подтвержден")
            await self.show_all_orders(query, db)
        else:
            await query.answer("Ошибка при подтверждении заказа", show_alert=True)
    
    async def admin_ship_order(self, query, db, order_id):
        """Admin ship order"""
        order_service = OrderService(db)
        
        order = order_service.update_order_status(order_id, OrderStatus.SHIPPED)
        if order:
            await query.answer("Заказ отправлен")
            await self.show_all_orders(query, db)
        else:
            await query.answer("Ошибка при отправке заказа", show_alert=True)
    
    async def admin_deliver_order(self, query, db, order_id):
        """Admin mark order as delivered"""
        order_service = OrderService(db)
        
        order = order_service.update_order_status(order_id, OrderStatus.DELIVERED)
        if order:
            await query.answer("Заказ доставлен")
            await self.show_all_orders(query, db)
        else:
            await query.answer("Ошибка при обновлении статуса", show_alert=True)
    
    async def admin_cancel_order(self, query, db, order_id):
        """Admin cancel order"""
        order_service = OrderService(db)
        
        order = order_service.update_order_status(order_id, OrderStatus.CANCELLED)
        if order:
            await query.answer("Заказ отменен")
            await self.show_all_orders(query, db)
        else:
            await query.answer("Ошибка при отмене заказа", show_alert=True)
    
    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        user = update.effective_user
        text = update.message.text
        
        user_state = self.get_user_state(user.id)
        current_state = user_state.get('state')
        
        if current_state == "checkout_contact_info":
            await self.process_contact_info(update, context, user, text)
        else:
            # Default response for unrecognized messages
            await update.message.reply_text(
                "Используйте кнопки меню для навигации или команду /help для справки."
            )
    
    async def process_contact_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user, text):
        """Process contact information during checkout"""
        db = get_db_session()
        
        try:
            # Parse contact info (simple parsing)
            parts = text.split(',')
            if len(parts) < 3:
                await update.message.reply_text(
                    "Неверный формат. Введите: Имя Фамилия, Телефон, Адрес"
                )
                return
            
            name = parts[0].strip()
            phone = parts[1].strip()
            address = parts[2].strip()
            
            # Get user state
            user_state = self.get_user_state(user.id)
            delivery_method = user_state.get('delivery_method', 'pickup')
            
            # Create order
            user_service = UserService(db)
            order_service = OrderService(db)
            
            db_user = user_service.get_user_by_telegram_id(user.id)
            if not db_user:
                await update.message.reply_text("Пользователь не найден.")
                return
            
            # Create order data
            order_data = OrderCreate(
                delivery_method=DeliveryMethod(delivery_method),
                delivery_address=address,
                customer_name=name,
                customer_phone=phone
            )
            
            # Create order
            order = order_service.create_order(db_user.id, order_data)
            
            # Show order confirmation
            text = f"""
📋 *Подтверждение заказа*

🆔 Номер заказа: {order.order_number}
👤 Имя: {name}
📞 Телефон: {phone}
🚚 Доставка: {delivery_method}
📍 Адрес: {address}
💰 Сумма: {order.total_amount:.2f} ₽

Подтвердите заказ:
            """
            
            keyboard = KeyboardBuilder.order_confirmation_keyboard(order.id)
            await update.message.reply_text(
                text,
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Clear user state
            self.clear_user_state(user.id)
            
        except Exception as e:
            logger.error(f"Error processing contact info: {e}")
            await update.message.reply_text("Произошла ошибка при обработке заказа.")
        finally:
            db.close()
