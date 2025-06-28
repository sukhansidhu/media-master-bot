from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.handlers import CallbackQueryHandler
from utils.buttons import back_button

async def forwarder_callback(client, callback_query: CallbackQuery):
    """Handle forwarder callback"""
    try:
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
    except Exception as e:
        await callback_query.answer(f"Error: {e}", show_alert=True)
        raise

async def forward_now_callback(client, callback_query: CallbackQuery):
    """Handle actual forwarding"""
    try:
        message_id = int(callback_query.data.split("_")[-1])
        chat_id = callback_query.message.chat.id
        
        # Forward the message
        await client.forward_messages(
            chat_id=chat_id,
            from_chat_id=chat_id,
            message_ids=[message_id]
        )
        
        await callback_query.answer("Message forwarded!")
        await callback_query.message.delete()
    except Exception as e:
        await callback_query.answer(f"Forward failed: {e}", show_alert=True)
        raise

def forwarder_handler():
    """Return list of forwarder handlers"""
    return [
        CallbackQueryHandler(forwarder_callback, filters.regex(r"^forwarder_")),
        CallbackQueryHandler(forward_now_callback, filters.regex(r"^forward_now_"))
    ]
