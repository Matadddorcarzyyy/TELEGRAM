"""
Database initialization script with sample data
"""
import logging
from sqlalchemy.orm import Session

from database import create_tables, get_db_session
from services import CategoryService, ProductService, UserService
from models import CategoryCreate, ProductCreate
from config import settings

logger = logging.getLogger(__name__)


def init_sample_data():
    """Initialize database with sample data"""
    db = get_db_session()
    
    try:
        # Create tables
        create_tables()
        logger.info("Database tables created")
        
        # Initialize services
        category_service = CategoryService(db)
        product_service = ProductService(db)
        
        # Check if data already exists
        existing_categories = category_service.get_all_categories()
        if existing_categories:
            logger.info("Sample data already exists, skipping initialization")
            return
        
        # Create sample categories
        categories_data = [
            CategoryCreate(
                name="Электроника",
                description="Смартфоны, планшеты, ноутбуки и другая электронная техника"
            ),
            CategoryCreate(
                name="Одежда",
                description="Мужская, женская и детская одежда"
            ),
            CategoryCreate(
                name="Дом и сад",
                description="Товары для дома, сада и интерьера"
            ),
            CategoryCreate(
                name="Спорт",
                description="Спортивные товары и аксессуары"
            ),
            CategoryCreate(
                name="Книги",
                description="Художественная и техническая литература"
            )
        ]
        
        created_categories = []
        for cat_data in categories_data:
            category = category_service.create_category(cat_data)
            created_categories.append(category)
            logger.info(f"Created category: {category.name}")
        
        # Create sample products
        products_data = [
            # Электроника
            ProductCreate(
                name="iPhone 15 Pro",
                description="Новейший смартфон от Apple с титановым корпусом и камерой 48 МП",
                price=99990.0,
                photo_url="https://example.com/iphone15pro.jpg",
                stock_quantity=10,
                category_id=created_categories[0].id
            ),
            ProductCreate(
                name="Samsung Galaxy S24",
                description="Флагманский Android смартфон с искусственным интеллектом",
                price=89990.0,
                photo_url="https://example.com/galaxys24.jpg",
                stock_quantity=15,
                category_id=created_categories[0].id
            ),
            ProductCreate(
                name="MacBook Air M3",
                description="Ультратонкий ноутбук с чипом M3 и дисплеем Liquid Retina",
                price=129990.0,
                photo_url="https://example.com/macbookair.jpg",
                stock_quantity=5,
                category_id=created_categories[0].id
            ),
            
            # Одежда
            ProductCreate(
                name="Джинсы Levi's 501",
                description="Классические прямые джинсы из денима премиум качества",
                price=5990.0,
                photo_url="https://example.com/levis501.jpg",
                stock_quantity=25,
                category_id=created_categories[1].id
            ),
            ProductCreate(
                name="Куртка The North Face",
                description="Теплая зимняя куртка с пуховым наполнителем",
                price=15990.0,
                photo_url="https://example.com/northface.jpg",
                stock_quantity=12,
                category_id=created_categories[1].id
            ),
            ProductCreate(
                name="Платье Zara",
                description="Элегантное вечернее платье из качественной ткани",
                price=3990.0,
                photo_url="https://example.com/zara-dress.jpg",
                stock_quantity=8,
                category_id=created_categories[1].id
            ),
            
            # Дом и сад
            ProductCreate(
                name="Кофемашина De'Longhi",
                description="Автоматическая кофемашина для приготовления эспрессо и капучино",
                price=45990.0,
                photo_url="https://example.com/delonghi.jpg",
                stock_quantity=3,
                category_id=created_categories[2].id
            ),
            ProductCreate(
                name="Набор кастрюль Tefal",
                description="Набор из 5 кастрюль с антипригарным покрытием",
                price=8990.0,
                photo_url="https://example.com/tefal.jpg",
                stock_quantity=7,
                category_id=created_categories[2].id
            ),
            ProductCreate(
                name="Садовые инструменты",
                description="Набор садовых инструментов: лопата, грабли, секатор",
                price=2990.0,
                photo_url="https://example.com/garden-tools.jpg",
                stock_quantity=20,
                category_id=created_categories[2].id
            ),
            
            # Спорт
            ProductCreate(
                name="Беговые кроссовки Nike Air Max",
                description="Комфортные кроссовки для бега с технологией Air Max",
                price=12990.0,
                photo_url="https://example.com/nike-airmax.jpg",
                stock_quantity=18,
                category_id=created_categories[3].id
            ),
            ProductCreate(
                name="Гантели 20кг",
                description="Разборные гантели для домашних тренировок",
                price=4990.0,
                photo_url="https://example.com/dumbbells.jpg",
                stock_quantity=6,
                category_id=created_categories[3].id
            ),
            ProductCreate(
                name="Йога-мат Liforme",
                description="Экологичный коврик для йоги с анатомическими линиями",
                price=6990.0,
                photo_url="https://example.com/yoga-mat.jpg",
                stock_quantity=14,
                category_id=created_categories[3].id
            ),
            
            # Книги
            ProductCreate(
                name="1984 - Джордж Оруэлл",
                description="Классический роман-антиутопия о тоталитарном обществе",
                price=590.0,
                photo_url="https://example.com/1984.jpg",
                stock_quantity=30,
                category_id=created_categories[4].id
            ),
            ProductCreate(
                name="Гарри Поттер и философский камень",
                description="Первая книга знаменитой серии о юном волшебнике",
                price=890.0,
                photo_url="https://example.com/harry-potter.jpg",
                stock_quantity=25,
                category_id=created_categories[4].id
            ),
            ProductCreate(
                name="Python для начинающих",
                description="Подробное руководство по изучению программирования на Python",
                price=1290.0,
                photo_url="https://example.com/python-book.jpg",
                stock_quantity=12,
                category_id=created_categories[4].id
            )
        ]
        
        for prod_data in products_data:
            product = product_service.create_product(prod_data)
            logger.info(f"Created product: {product.name}")
        
        logger.info("Sample data initialization completed successfully")
        
    except Exception as e:
        logger.error(f"Error initializing sample data: {e}")
        raise
    finally:
        db.close()


def main():
    """Main function"""
    try:
        init_sample_data()
        print("✅ Database initialized with sample data successfully!")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        raise


if __name__ == "__main__":
    main()
