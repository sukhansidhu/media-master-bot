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
    
    # Import all media handlers directly
    from handlers.audio_tools import handlers as audio_handlers
    from handlers.caption_editor import handlers as caption_handlers
    from handlers.converter import handlers as converter_handlers
    from handlers.forwarder import handlers as forwarder_handlers
    from handlers.media_info import handlers as media_info_handlers
    from handlers.metadata_editor import handlers as metadata_handlers
    from handlers.renamer import handlers as renamer_handlers
    from handlers.screenshot import handlers as screenshot_handlers
    from handlers.stream_tools import handlers as stream_handlers
    from handlers.video_merge import handlers as video_merge_handlers
    from handlers.video_trimmer import handlers as video_trimmer_handlers
    
    # Combine all media handlers into one list
    media_handlers = (
        audio_handlers +
        caption_handlers +
        converter_handlers +
        forwarder_handlers +
        media_info_handlers +
        metadata_handlers +
        renamer_handlers +
        screenshot_handlers +
        stream_handlers +
        video_merge_handlers +
        video_trimmer_handlers
    )
    
    logger.info("All handlers imported successfully")
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error(traceback.format_exc())
    sys.exit(1)

# Initialize Pyrogram client
app = Client(
    "media_master_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# Initialize database
db = Database()

# Register handlers
try:
    app.add_handler(start_handler)
    app.add_handler(settings_handler)
    app.add_handler(admin_handler)
    app.add_handler(progress_handler)
    app.add_handler(utilities_handler)
    
    # Register all media tools handlers
    for handler in media_handlers:
        app.add_handler(handler)
        
    logger.info("All handlers registered successfully")
except Exception as e:
    logger.error(f"Handler registration error: {e}")
    logger.error(traceback.format_exc())
    sys.exit(1)

@app.on_message(filters.document | filters.video | filters.audio)
async def handle_media(client: Client, message: Message):
    """Handle incoming media files and show processing options"""
    user_id = message.from_user.id
    is_premium = False  # Placeholder
    
    buttons = get_media_options(message, is_premium)
    
    await message.reply_text(
        "📁 **Media Received**\nSelect an action:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

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
