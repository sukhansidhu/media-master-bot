from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.handlers import MessageHandler
from utils.buttons import start_markup

async def start_command(client, message: Message):
    """Handle /start command"""
    await message.reply_text(
        "🎬 **Media Master Bot**\n\n"
        "A powerful media processing bot with advanced features:\n"
        "- Video editing tools\n"
        "- Audio processing\n"
        "- Document conversion\n"
        "- And much more!\n\n"
        "Send me a media file to get started!",
        reply_markup=start_markup()
    )

start_handler = MessageHandler(start_command, filters.command("start") & filters.private)
