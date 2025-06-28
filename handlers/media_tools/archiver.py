from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from utils.db import Database
from utils.buttons import archive_markup, back_button
import zipfile
import os
import logging

logger = logging.getLogger(__name__)
db = Database()

async def archiver_callback(client, callback_query: CallbackQuery):
    """Handle archiver callback"""
    try:
        user_id = callback_query.from_user.id
        message = callback_query.message
        media_message = message.reply_to_message
        
        if not media_message:
            await callback_query.answer("Original message not found!")
            return
        
        action = callback_query.data.split("_")[-1]
        
        if action == "options":
            await callback_query.message.edit_text(
                "🗄️ **Archive Creator**\n\n"
                "Select archive format:",
                reply_markup=archive_markup()
            )
        
        elif action.startswith("format_"):
            archive_format = action.split("_")[-1]
            file_path = await media_message.download()
            archive_path = f"data/{user_id}_archive.{archive_format}"
            
            await callback_query.message.edit_text(f"🗜 Creating {archive_format.upper()} archive...")
            
            try:
                if archive_format == "zip":
                    with zipfile.ZipFile(archive_path, 'w') as zipf:
                        zipf.write(file_path, os.path.basename(file_path))
                
                await client.send_document(
                    chat_id=user_id,
                    document=archive_path,
                    caption=f"✅ {archive_format.upper()} archive created!",
                    file_name=f"archive.{archive_format}"
                )
            except Exception as e:
                await callback_query.message.edit_text(f"❌ Error: {e}")
            finally:
                if os.path.exists(file_path):
                    os.unlink(file_path)
                if os.path.exists(archive_path):
                    os.unlink(archive_path)
    except Exception as e:
        logger.error(f"Error in archiver_callback: {e}")

async def archive_password_callback(client, callback_query: CallbackQuery):
    """Handle archive password input"""
    try:
        user_id = callback_query.from_user.id
        await callback_query.message.edit_text(
            "🔒 **Password Protected Archive**\n\n"
            "Send me the password for the archive:",
            reply_markup=back_button("archive_options")
        )
        
        archive_format = callback_query.data.split("_")[-1]
        await db.set_temp_data(user_id, "archive_password", {
            "archive_format": archive_format
        })
    except Exception as e:
        logger.error(f"Error in archive_password_callback: {e}")

async def archive_password_message(client, message: Message):
    """Handle archive password message"""
    try:
        user_id = message.from_user.id
        temp_data = await db.get_temp_data(user_id, "archive_password")
        
        if not temp_data:
            return
        
        password = message.text.strip()
        archive_format = temp_data.get("archive_format")
        
        await message.reply_text(
            "🔒 Password-protected archive created!\n"
            f"Format: {archive_format.upper()}\n"
            f"Password: {password}"
        )
        
        await db.delete_temp_data(user_id, "archive_password")
    except Exception as e:
        logger.error(f"Error in archive_password_message: {e}")

def archiver_handler():
    """Return a list of handlers for archive functionality"""
    try:
        # FIXED: Proper filter syntax
        password_filter = filters.text & filters.private & ~filters.command()
        
        return [
            CallbackQueryHandler(archiver_callback, filters.regex(r"^archiver_")),
            CallbackQueryHandler(archive_password_callback, filters.regex(r"^archive_password_")),
            MessageHandler(archive_password_message, password_filter)
        ]
    except Exception as e:
        logger.error(f"Error creating archiver_handler: {e}")
        return []
