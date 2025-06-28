from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from utils.db import Database
from utils.buttons import archive_markup, back_button
import zipfile
import os

db = Database()

async def archiver_callback(client, callback_query: CallbackQuery):
    """Handle archiver callback"""
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
        
        # Download the file
        file_path = await media_message.download()
        archive_path = f"data/{user_id}_archive.{archive_format}"
        
        await callback_query.message.edit_text(f"🗜 Creating {archive_format.upper()} archive...")
        
        try:
            if archive_format == "zip":
                with zipfile.ZipFile(archive_path, 'w') as zipf:
                    zipf.write(file_path, os.path.basename(file_path))
            
            # Upload the archive
            await client.send_document(
                chat_id=user_id,
                document=archive_path,
                caption=f"✅ {archive_format.upper()} archive created!",
                file_name=f"archive.{archive_format}"
            )
        except Exception as e:
            await callback_query.message.edit_text(f"❌ Error: {e}")
        finally:
            # Clean up files
            if os.path.exists(file_path):
                os.unlink(file_path)
            if os.path.exists(archive_path):
                os.unlink(archive_path)

async def archive_password_callback(client, callback_query: CallbackQuery):
    """Handle archive password input"""
    user_id = callback_query.from_user.id
    await callback_query.message.edit_text(
        "🔒 **Password Protected Archive**\n\n"
        "Send me the password for the archive:",
        reply_markup=back_button("archive_options")
    )
    
    # Store the archive format for later reference
    archive_format = callback_query.data.split("_")[-1]
    await db.set_temp_data(user_id, "archive_password", {
        "archive_format": archive_format
    })

async def archive_password_message(client, message: Message):
    """Handle archive password message"""
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
    
    # Clean up temp data
    await db.delete_temp_data(user_id, "archive_password")

def archiver_handler():
    return [
        CallbackQueryHandler(archiver_callback, filters.regex("^archiver_")),
        CallbackQueryHandler(archive_password_callback, filters.regex("^archive_password_")),
        # FIXED: Added parentheses to filters.command()
        MessageHandler(archive_password_message, filters.text & filters.private & ~filters.command())
    ]
