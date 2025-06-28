import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup
from config import Config
from handlers.start import start_handler
from handlers.settings import settings_handler
from handlers.admin import admin_handler
from handlers.progress import progress_handler
from handlers.utilities import utilities_handler
from handlers.media_tools import media_handlers  # Import the list directly
from utils.db import Database
from utils.buttons import media_tools_options
from utils.progress import progress_callback

# Initialize logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
app.add_handler(start_handler)
app.add_handler(settings_handler)
app.add_handler(admin_handler)
app.add_handler(progress_handler)
app.add_handler(utilities_handler)

# Register media tools handlers
for handler in media_handlers:  # Use the imported list directly
    app.add_handler(handler)

@app.on_message(filters.document | filters.video | filters.audio)
async def handle_media(client: Client, message: Message):
    """Handle incoming media files and show processing options"""
    user_id = message.from_user.id
    
    # Check if user is premium
    is_premium = await db.is_premium_user(user_id)
    
    # Get appropriate buttons based on media type
    buttons = get_media_options(message, is_premium)
    
    await message.reply_text(
        "📁 **Media Received**\nSelect an action:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

if __name__ == "__main__":
    # Create data directory if not exists
    os.makedirs("data", exist_ok=True)
    
    logger.info("Starting Media Master Bot...")
    app.run()
