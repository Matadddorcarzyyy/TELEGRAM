#!/usr/bin/env python3
"""
Test runner script for the E-commerce Telegram Bot
"""
import sys
import subprocess
import os
from pathlib import Path


def run_tests():
    """Run all tests with proper configuration"""
    
    # Set test environment
    os.environ['DATABASE_URL'] = 'sqlite:///./test.db'
    os.environ['DEBUG'] = 'True'
    os.environ['LOG_LEVEL'] = 'WARNING'  # Reduce log noise during tests
    
    # Test command
    test_command = [
        sys.executable, '-m', 'pytest',
        'tests.py',
        '-v',  # Verbose output
        '--tb=short',  # Short traceback format
        '--disable-warnings',  # Disable warnings
        '--color=yes'  # Colored output
    ]
    
    print("🧪 Запуск тестов...")
    print(f"Команда: {' '.join(test_command)}")
    print("-" * 50)
    
    try:
        # Run tests
        result = subprocess.run(test_command, check=True)
        
        print("-" * 50)
        print("✅ Все тесты прошли успешно!")
        return True
        
    except subprocess.CalledProcessError as e:
        print("-" * 50)
        print(f"❌ Тесты завершились с ошибкой (код: {e.returncode})")
        return False
        
    except FileNotFoundError:
        print("❌ pytest не найден. Установите его: pip install pytest")
        return False


def run_specific_test(test_name):
    """Run specific test"""
    os.environ['DATABASE_URL'] = 'sqlite:///./test.db'
    os.environ['DEBUG'] = 'True'
    os.environ['LOG_LEVEL'] = 'WARNING'
    
    test_command = [
        sys.executable, '-m', 'pytest',
        f'tests.py::{test_name}',
        '-v',
        '--tb=short',
        '--disable-warnings',
        '--color=yes'
    ]
    
    print(f"🧪 Запуск теста: {test_name}")
    print(f"Команда: {' '.join(test_command)}")
    print("-" * 50)
    
    try:
        result = subprocess.run(test_command, check=True)
        print("-" * 50)
        print(f"✅ Тест {test_name} прошел успешно!")
        return True
        
    except subprocess.CalledProcessError as e:
        print("-" * 50)
        print(f"❌ Тест {test_name} завершился с ошибкой")
        return False


def run_coverage():
    """Run tests with coverage report"""
    try:
        import coverage
    except ImportError:
        print("❌ coverage не установлен. Установите его: pip install coverage")
        return False
    
    os.environ['DATABASE_URL'] = 'sqlite:///./test.db'
    os.environ['DEBUG'] = 'True'
    os.environ['LOG_LEVEL'] = 'WARNING'
    
    print("🧪 Запуск тестов с покрытием кода...")
    
    # Run coverage
    coverage_command = [
        sys.executable, '-m', 'coverage', 'run', '-m', 'pytest', 'tests.py', '-v'
    ]
    
    try:
        subprocess.run(coverage_command, check=True)
        
        # Generate report
        report_command = [sys.executable, '-m', 'coverage', 'report']
        subprocess.run(report_command, check=True)
        
        # Generate HTML report
        html_command = [sys.executable, '-m', 'coverage', 'html']
        subprocess.run(html_command, check=True)
        
        print("✅ Отчет о покрытии кода создан в htmlcov/index.html")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при запуске тестов с покрытием: {e}")
        return False


def main():
    """Main function"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "coverage":
            success = run_coverage()
        elif command.startswith("test:"):
            test_name = command.split(":", 1)[1]
            success = run_specific_test(test_name)
        else:
            print(f"❌ Неизвестная команда: {command}")
            print("Доступные команды:")
            print("  python run_tests.py          - Запустить все тесты")
            print("  python run_tests.py coverage - Запустить тесты с покрытием")
            print("  python run_tests.py test:TestName - Запустить конкретный тест")
            return False
    else:
        success = run_tests()
    
    # Cleanup test database
    test_db = Path("test.db")
    if test_db.exists():
        test_db.unlink()
        print("🧹 Тестовая база данных удалена")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
