"""
Main bot application for the E-commerce Telegram Bot
"""
import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram.constants import ParseMode

from config import settings
from database import create_tables
from handlers import BotHandlers
from utils import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


class EcommerceBot:
    """Main bot class"""
    
    def __init__(self):
        self.handlers = BotHandlers()
        self.application = None
    
    def setup_handlers(self):
        """Setup bot handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.handlers.start_command))
        self.application.add_handler(CommandHandler("help", self.handlers.help_command))
        self.application.add_handler(CommandHandler("admin", self.handlers.admin_command))
        
        # Callback query handler
        self.application.add_handler(CallbackQueryHandler(self.handlers.callback_query_handler))
        
        # Message handler
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handlers.message_handler))
        
        logger.info("Bot handlers setup completed")
    
    def setup_error_handler(self):
        """Setup error handler"""
        async def error_handler(update, context):
            """Handle errors"""
            logger.error(f"Update {update} caused error {context.error}")
            
            if update and update.effective_message:
                await update.effective_message.reply_text(
                    "Произошла ошибка. Попробуйте позже или обратитесь к администратору."
                )
        
        self.application.add_error_handler(error_handler)
        logger.info("Error handler setup completed")
    
    async def post_init(self, application):
        """Post initialization tasks"""
        # Create database tables
        create_tables()
        logger.info("Database tables created")
        
        # Send startup message to admin
        if settings.admin_user_id:
            try:
                await application.bot.send_message(
                    chat_id=settings.admin_user_id,
                    text="🤖 E-commerce Bot запущен и готов к работе!"
                )
            except Exception as e:
                logger.warning(f"Could not send startup message to admin: {e}")
    
    def run(self):
        """Run the bot"""
        try:
            # Create application
            self.application = Application.builder().token(settings.bot_token).build()
            
            # Setup handlers
            self.setup_handlers()
            self.setup_error_handler()
            
            # Post initialization
            self.application.post_init = self.post_init
            
            logger.info("Starting E-commerce Bot...")
            
            # Run the bot
            self.application.run_polling(
                allowed_updates=["message", "callback_query"],
                drop_pending_updates=True
            )
            
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            raise


def main():
    """Main function"""
    try:
        bot = EcommerceBot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        raise


if __name__ == "__main__":
    main()
