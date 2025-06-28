import os
import logging
import sys
import traceback
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup
from config import Config
from utils.db import Database
from utils.buttons import get_media_options
from utils.progress import progress_callback

# Initialize logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    # Import core handlers
    from handlers.start import start_handler
    from handlers.settings import settings_handler
    from handlers.admin import admin_handler
    from handlers.progress import progress_handler
    from handlers.utilities import utilities_handler
    
    # Import media tools handlers
    from handlers.media_tools import media_handlers
    
    logger.info("All handlers imported successfully")
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error(traceback.format_exc())
    media_handlers = []

# Initialize Pyrogram client
app = Client(
    "media_master_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# Initialize database
db = Database()

# Register core handlers
try:
    app.add_handler(start_handler)
    app.add_handler(settings_handler)
    app.add_handler(admin_handler)
    app.add_handler(progress_handler)
    app.add_handler(utilities_handler)
    logger.info("Core handlers registered successfully")
except Exception as e:
    logger.error(f"Core handler registration error: {e}")
    logger.error(traceback.format_exc())

# Register media tools handlers with robust error handling
if media_handlers:
    for handler in media_handlers:
        try:
            app.add_handler(handler)
        except Exception as e:
            logger.error(f"Failed to register media handler: {e}")
            logger.error(traceback.format_exc())
    logger.info(f"Registered {len(media_handlers)} media handlers")
else:
    logger.warning("No media handlers to register")

@app.on_message(filters.document | filters.video | filters.audio)
async def handle_media(client: Client, message: Message):
    """Handle incoming media files and show processing options"""
    try:
        user_id = message.from_user.id
        is_premium = False  # Placeholder
        
        buttons = get_media_options(message, is_premium)
        
        # FIXED: Properly closed parentheses
        await message.reply_text(
            "📁 **Media Received**\nSelect an action:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        logger.error(f"Error handling media: {e}")
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    # Create data directory if not exists
    os.makedirs("data", exist_ok=True)
    
    logger.info("Starting Media Master Bot...")
    try:
        app.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)
