"""
Utility functions for the E-commerce Telegram Bot
"""
import logging
import sys
from pathlib import Path
from loguru import logger as loguru_logger
from config import settings


def setup_logging():
    """Setup logging configuration"""
    # Remove default loguru handler
    loguru_logger.remove()
    
    # Add console handler
    loguru_logger.add(
        sys.stdout,
        level=settings.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True
    )
    
    # Add file handler
    log_file = Path("logs") / "bot.log"
    log_file.parent.mkdir(exist_ok=True)
    
    loguru_logger.add(
        log_file,
        level=settings.log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="1 day",
        retention="30 days",
        compression="zip"
    )
    
    # Intercept standard logging
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            try:
                level = loguru_logger.level(record.levelname).name
            except ValueError:
                level = record.levelno
            
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1
            
            loguru_logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )
    
    # Setup standard logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    
    # Set specific loggers
    logging.getLogger("telegram").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING if not settings.debug else logging.INFO)


def format_price(price: float) -> str:
    """Format price for display"""
    return f"{price:.2f} ₽"


def format_phone(phone: str) -> str:
    """Format phone number for display"""
    # Simple phone formatting
    phone = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    if phone.startswith("+7"):
        return f"+7({phone[2:5]}){phone[5:8]}-{phone[8:10]}-{phone[10:12]}"
    elif phone.startswith("8") and len(phone) == 11:
        return f"+7({phone[1:4]}){phone[4:7]}-{phone[7:9]}-{phone[9:11]}"
    return phone


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    import re
    # Russian phone number pattern
    pattern = r'^(\+7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'
    return bool(re.match(pattern, phone))


def validate_email(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def generate_order_number() -> str:
    """Generate unique order number"""
    import uuid
    import datetime
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid.uuid4())[:8].upper()
    return f"ORD-{timestamp}-{unique_id}"


def calculate_delivery_cost(delivery_method: str, total_amount: float) -> float:
    """Calculate delivery cost based on method and order amount"""
    if delivery_method == "pickup":
        return 0.0
    elif delivery_method == "courier":
        return 300.0 if total_amount < 2000 else 0.0
    elif delivery_method == "post":
        return 200.0 if total_amount < 1500 else 0.0
    return 0.0


def get_delivery_time(delivery_method: str) -> str:
    """Get estimated delivery time"""
    delivery_times = {
        "pickup": "1-2 часа",
        "courier": "1-3 дня",
        "post": "3-7 дней"
    }
    return delivery_times.get(delivery_method, "Уточняется")


def format_delivery_method(method: str) -> str:
    """Format delivery method for display"""
    method_names = {
        "pickup": "🏪 Самовывоз",
        "courier": "🚚 Курьерская доставка",
        "post": "📮 Почтовая доставка"
    }
    return method_names.get(method, method)


def format_order_status(status: str) -> str:
    """Format order status for display"""
    status_names = {
        "pending": "⏳ Ожидает подтверждения",
        "confirmed": "✅ Подтвержден",
        "shipped": "🚚 Отправлен",
        "delivered": "📦 Доставлен",
        "cancelled": "❌ Отменен"
    }
    return status_names.get(status, status)


def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id == settings.admin_user_id


def escape_markdown(text: str) -> str:
    """Escape special characters for Markdown"""
    import re
    # Escape special Markdown characters
    special_chars = r'[_*[\]()~`>#+=|{}.!-]'
    return re.sub(special_chars, r'\\\g<0>', text)


def format_product_list(products: list, max_items: int = 10) -> str:
    """Format product list for display"""
    if not products:
        return "Товары не найдены."
    
    text = "📦 *Список товаров:*\n\n"
    
    for i, product in enumerate(products[:max_items], 1):
        text += f"{i}. 🛍️ *{product.name}*\n"
        text += f"   💰 {format_price(product.price)}\n"
        text += f"   📦 В наличии: {product.stock_quantity} шт.\n\n"
    
    if len(products) > max_items:
        text += f"... и еще {len(products) - max_items} товаров"
    
    return text


def format_category_list(categories: list) -> str:
    """Format category list for display"""
    if not categories:
        return "Категории не найдены."
    
    text = "📁 *Категории товаров:*\n\n"
    
    for i, category in enumerate(categories, 1):
        text += f"{i}. 📁 *{category.name}*\n"
        if category.description:
            text += f"   📝 {truncate_text(category.description, 100)}\n"
        text += "\n"
    
    return text


def format_order_summary(order) -> str:
    """Format order summary for display"""
    text = f"""
📋 *Заказ #{order.order_number}*

👤 *Клиент:* {order.customer_name}
📞 *Телефон:* {format_phone(order.customer_phone)}
🚚 *Доставка:* {format_delivery_method(order.delivery_method)}
📍 *Адрес:* {order.delivery_address}

📦 *Товары:*
"""
    
    for item in order.order_items:
        text += f"• {item.product.name} x{item.quantity} = {format_price(item.price * item.quantity)}\n"
    
    text += f"""
💰 *Итого:* {format_price(order.total_amount)}
📊 *Статус:* {format_order_status(order.status)}
📅 *Дата:* {order.created_at.strftime('%d.%m.%Y %H:%M')}
"""
    
    if order.notes:
        text += f"\n📝 *Примечания:* {order.notes}"
    
    return text
