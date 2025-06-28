from pyrogram import filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from utils.buttons import back_button
from utils.db import Database

db = Database()

async def caption_editor_callback(client, callback_query: CallbackQuery):
    """Handle caption editor callback"""
    user_id = callback_query.from_user.id
    message = callback_query.message
    media_message = message.reply_to_message
    
    if not media_message:
        await callback_query.answer("Original message not found!")
        return
    
    await callback_query.message.edit_text(
        "✏️ **Caption Editor**\n\n"
        "Send me the new caption for this media:",
        reply_markup=back_button("media_options")
    )
    
    # Store the media message ID for later reference
    await db.set_temp_data(user_id, "caption_editor", {
        "media_message_id": media_message.id
    })

async def caption_editor_message(client, message: Message):
    """Handle new caption message"""
    user_id = message.from_user.id
    temp_data = await db.get_temp_data(user_id, "caption_editor")
    
    if not temp_data:
        return
    
    media_message_id = temp_data.get("media_message_id")
    media_message = await client.get_messages(message.chat.id, media_message_id)
    
    if not media_message:
        await message.reply_text("Original media message not found!")
        return
    
    # Edit the media message with new caption
    try:
        await media_message.edit_caption(message.text)
        await message.reply_text("✅ Caption updated successfully!")
    except Exception as e:
        await message.reply_text(f"❌ Failed to update caption: {e}")
    
    # Clean up temp data
    await db.delete_temp_data(user_id, "caption_editor")

def caption_editor_handler():
    return [
        CallbackQueryHandler(caption_editor_callback, filters.regex("^caption_editor_")),
        MessageHandler(caption_editor_message, filters.text & filters.private)
    ]
