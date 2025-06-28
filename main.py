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

# Register media tools handlers
if media_handlers:
    for handler in media_handlers:
        try:
            app.add_handler(handler)
            logger.debug(f"Registered handler: {type(handler).__name__}")
        except Exception as e:
            logger.error(f"Failed to register media handler: {e}")
            logger.error(traceback.format_exc())
    logger.info(f"Registered {len(media_handlers)} media handlers")
else:
    logger.warning("No media handlers to register")

# Test command to verify bot is working
@app.on_message(filters.command("test"))
async def test_command(client: Client, message: Message):
    try:
        await message.reply("✅ Bot is working and responding!")
        logger.info("Test command executed successfully")
    except Exception as e:
        logger.error(f"Test command failed: {e}")

@app.on_message(filters.document | filters.video | filters.audio)
async def handle_media(client: Client, message: Message):
    """Handle incoming media files and show processing options"""
    try:
        logger.info(f"Received media from {message.from_user.id} ({message.from_user.first_name})")
        
        # Get actual media type and file name
        media_type = "unknown"
        file_name = "N/A"
        
        if message.document:
            media_type = "document"
            file_name = message.document.file_name
        elif message.video:
            media_type = "video"
            file_name = message.video.file_name
        elif message.audio:
            media_type = "audio"
            file_name = message.audio.file_name
        
        logger.info(f"Media type: {media_type}")
        logger.info(f"File name: {file_name}")
        
        user_id = message.from_user.id
        is_premium = False
        
        buttons = get_media_options(message, is_premium)
        
        response = await message.reply_text(
            "📁 **Media Received**\nSelect an action:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        
        logger.info(f"Media options sent successfully (message ID: {response.id})")
    except Exception as e:
        logger.error(f"Error handling media: {e}")
        logger.error(traceback.format_exc())

# Debug handler to log callback queries
# Add this to your existing main.py, right before app.run()

@app.on_callback_query()
async def handle_all_callbacks(client, callback_query):
    """Global callback handler for debugging"""
    try:
        logger.info(f"Callback received: {callback_query.data} from {callback_query.from_user.id}")
        
        # Check if any handler processed this callback
        processed = False
        for handler in app.dispatcher.handlers[1]:  # Callback query handlers
            if await handler.check(client, callback_query):
                processed = True
                break
                
        if not processed:
            await callback_query.answer("⚠️ No handler found for this action", show_alert=True)
            logger.warning(f"No handler found for callback: {callback_query.data}")
            
    except Exception as e:
        logger.error(f"Error in global callback handler: {e}")
        await callback_query.answer("❌ An error occurred", show_alert=True)

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
