from pyrogram import filters
from pyrogram.types import CallbackQuery
from pyrogram.handlers import CallbackQueryHandler

async def forwarder_callback(client, callback_query: CallbackQuery):
    """Handle forwarder callback"""
    message = callback_query.message
    media_message = message.reply_to_message
    
    if not media_message:
        await callback_query.answer("Original message not found!")
        return
    
    await callback_query.message.edit_text(
        "📤 **Forwarder**\n\n"
        "Forward this media to another chat?",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Yes, forward now", callback_data=f"forward_now_{media_message.id}")],
            [back_button("media_options")]
        ])
    )

def forwarder_handler():
    return CallbackQueryHandler(forwarder_callback, filters.regex("^forwarder_"))
