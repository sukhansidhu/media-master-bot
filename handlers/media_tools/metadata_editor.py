from pyrogram import filters
from pyrogram.types import CallbackQuery
from pyrogram.handlers import CallbackQueryHandler
from utils.ffmpeg import edit_metadata
from utils.db import Database

db = Database()

async def metadata_editor_callback(client, callback_query: CallbackQuery):
    """Handle metadata editor callback"""
    user_id = callback_query.from_user.id
    message = callback_query.message
    media_message = message.reply_to_message
    
    if not media_message:
        await callback_query.answer("Original message not found!")
        return
    
    # Download the media file
    file_path = await media_message.download()
    
    # Show metadata editing options
    await callback_query.message.edit_text(
        "📝 **Metadata Editor**\n\n"
        "Select which metadata to edit:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Title", callback_data=f"meta_title_{media_message.id}")],
            [InlineKeyboardButton("Artist/Author", callback_data=f"meta_artist_{media_message.id}")],
            [InlineKeyboardButton("Custom Metadata", callback_data=f"meta_custom_{media_message.id}")],
            [back_button("media_options")]
        ])
    )

def metadata_editor_handler():
    return CallbackQueryHandler(metadata_editor_callback, filters.regex("^metadata_editor_"))
