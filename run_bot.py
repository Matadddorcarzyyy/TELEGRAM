#!/usr/bin/env python3
"""
Bot runner script with environment setup and error handling
"""
import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def check_requirements():
    """Check if all required packages are installed"""
    required_packages = [
        'telegram',
        'sqlalchemy',
        'pydantic',
        'loguru',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Отсутствуют необходимые пакеты:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nУстановите их командой:")
        print("pip install -r requirements.txt")
        return False
    
    return True


def check_environment():
    """Check environment variables"""
    required_vars = ['BOT_TOKEN', 'ADMIN_USER_ID']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Отсутствуют переменные окружения:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nСоздайте файл .env на основе env.example и заполните необходимые переменные")
        return False
    
    return True


def check_database():
    """Check if database is initialized"""
    db_file = Path("ecommerce_bot.db")
    
    if not db_file.exists():
        print("⚠️  База данных не найдена")
        response = input("Инициализировать базу данных с тестовыми данными? (y/n): ")
        
        if response.lower() in ['y', 'yes', 'да', 'д']:
            try:
                from init_db import init_sample_data
                print("🔄 Инициализация базы данных...")
                init_sample_data()
                print("✅ База данных инициализирована")
                return True
            except Exception as e:
                print(f"❌ Ошибка при инициализации базы данных: {e}")
                return False
        else:
            print("❌ База данных не инициализирована")
            return False
    
    return True


def setup_logging():
    """Setup logging configuration"""
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Configure logging
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/bot.log'),
            logging.StreamHandler()
        ]
    )


def main():
    """Main function"""
    print("🤖 E-commerce Telegram Bot")
    print("=" * 40)
    
    # Check requirements
    print("🔍 Проверка зависимостей...")
    if not check_requirements():
        return False
    
    # Check environment
    print("🔍 Проверка переменных окружения...")
    if not check_environment():
        return False
    
    # Check database
    print("🔍 Проверка базы данных...")
    if not check_database():
        return False
    
    # Setup logging
    setup_logging()
    
    print("✅ Все проверки пройдены")
    print("🚀 Запуск бота...")
    print("-" * 40)
    
    try:
        # Import and run bot
        from bot import main as bot_main
        bot_main()
        
    except KeyboardInterrupt:
        print("\n⏹️  Бот остановлен пользователем")
        return True
        
    except Exception as e:
        print(f"\n❌ Ошибка при запуске бота: {e}")
        logging.error(f"Bot startup error: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
