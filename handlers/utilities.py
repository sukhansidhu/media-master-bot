from pyrogram import filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler

async def utilities_command(client, message: Message):
    """Handle utilities commands"""
    command = message.command[0].lower()
    
    if command == "help":
        await message.reply_text(
            "🛠️ **Media Master Bot Help**\n\n"
            "Send me any media file (video, audio, document) to access processing options.\n\n"
            "**Commands:**\n"
            "/start - Start the bot\n"
            "/settings - Configure your preferences\n"
            "/help - Show this help message"
        )

utilities_handler = MessageHandler(utilities_command, filters.command(["help"]) & filters.private)
