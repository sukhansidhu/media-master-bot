from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from utils.buttons import settings_markup, back_button
from utils.db import Database

db = Database()

async def settings_command(client, message: Message):
    """Handle /settings command"""
    user_id = message.from_user.id
    user_settings = await db.get_user_settings(user_id)
    
    text = (
        "⚙️ **User Settings**\n\n"
        f"• **Upload Mode:** {user_settings.get('upload_mode', 'Streamable')}\n"
        f"• **Auto Rename:** {'Enabled' if user_settings.get('auto_rename', False) else 'Disabled'}\n"
        f"• **Default Format:** {user_settings.get('default_format', 'Original')}\n"
    )
    
    await message.reply_text(
        text,
        reply_markup=settings_markup()
    )

async def settings_callback(client, callback_query):
    """Handle settings callback queries"""
    data = callback_query.data
    user_id = callback_query.from_user.id
    
    if data == "settings_upload_mode":
        await db.update_user_settings(user_id, {"upload_mode": "Document"})
        await callback_query.answer("Upload mode set to Document")
    elif data == "settings_auto_rename":
        current = await db.get_user_settings(user_id)
        new_setting = not current.get("auto_rename", False)
        await db.update_user_settings(user_id, {"auto_rename": new_setting})
        status = "Enabled" if new_setting else "Disabled"
        await callback_query.answer(f"Auto rename {status}")
    elif data == "settings_back":
        await callback_query.message.delete()
        return
    
    # Update the settings message
    user_settings = await db.get_user_settings(user_id)
    text = (
        "⚙️ **User Settings**\n\n"
        f"• **Upload Mode:** {user_settings.get('upload_mode', 'Streamable')}\n"
        f"• **Auto Rename:** {'Enabled' if user_settings.get('auto_rename', False) else 'Disabled'}\n"
        f"• **Default Format:** {user_settings.get('default_format', 'Original')}\n"
    )
    
    await callback_query.message.edit_text(
        text,
        reply_markup=settings_markup()
    )

settings_handler = MessageHandler(settings_command, filters.command("settings") & filters.private)
settings_callback_handler = CallbackQueryHandler(settings_callback, filters.regex("^settings_"))
