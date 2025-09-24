"""
Configuration settings for the E-commerce Telegram Bot
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""
    
    # Bot Configuration
    bot_token: str = Field(..., env="BOT_TOKEN")
    admin_user_id: int = Field(..., env="ADMIN_USER_ID")
    
    # Database Configuration
    database_url: str = Field(default="sqlite:///./ecommerce_bot.db", env="DATABASE_URL")
    
    # Application Settings
    debug: bool = Field(default=False, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Bot Messages
    welcome_message: str = "🛍️ Добро пожаловать в наш интернет-магазин!\n\nВыберите категорию товаров:"
    cart_empty_message: str = "🛒 Ваша корзина пуста"
    order_success_message: str = "✅ Заказ успешно оформлен!"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
