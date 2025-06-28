from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from utils.db import Database
from utils.buttons import back_button

db = Database()

async def renamer_callback(client, callback_query: CallbackQuery):
    """Handle renamer callback"""
    user_id = callback_query.from_user.id
    message = callback_query.message
    media_message = message.reply_to_message
    
    if not media_message:
        await callback_query.answer("Original message not found!")
        return
    
    await callback_query.message.edit_text(
        "📝 **File Renamer**\n\n"
        "Send me the new file name (without extension):",
        reply_markup=back_button("media_options")
    )
    
    # Store the media message ID for later reference
    await db.set_temp_data(user_id, "file_renamer", {
        "media_message_id": media_message.id
    })

async def renamer_message(client, message: Message):
    """Handle new file name input"""
    user_id = message.from_user.id
    temp_data = await db.get_temp_data(user_id, "file_renamer")
    
    if not temp_data:
        return
    
    # Skip command messages
    if message.text.startswith('/'):
        return
    
    media_message_id = temp_data.get("media_message_id")
    media_message = await client.get_messages(message.chat.id, media_message_id)
    
    if not media_message:
        await message.reply_text("Original media message not found!")
        return
    
    new_name = message.text.strip()
    
    # Get file extension from original file
    if media_message.video:
        ext = media_message.video.file_name.split(".")[-1]
    elif media_message.audio:
        ext = media_message.audio.file_name.split(".")[-1]
    elif media_message.document:
        ext = media_message.document.file_name.split(".")[-1]
    else:
        ext = ""
    
    new_filename = f"{new_name}.{ext}" if ext else new_name
    
    # Download the file
    file_path = await media_message.download(file_name=new_filename)
    
    # Upload the renamed file
    try:
        if media_message.video:
            await client.send_video(
                chat_id=user_id,
                video=file_path,
                caption=f"✅ Renamed to: {new_filename}",
                file_name=new_filename
            )
        elif media_message.audio:
            await client.send_audio(
                chat_id=user_id,
                audio=file_path,
                caption=f"✅ Renamed to: {new_filename}",
                file_name=new_filename
            )
        else:
            await client.send_document(
                chat_id=user_id,
                document=file_path,
                caption=f"✅ Renamed to: {new_filename}",
                file_name=new_filename
            )
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
    finally:
        # Clean up file
        os.unlink(file_path)
    
    # Clean up temp data
    await db.delete_temp_data(user_id, "file_renamer")

def renamer_handler():
    return [
        CallbackQueryHandler(renamer_callback, filters.regex("^renamer_")),
        MessageHandler(renamer_message, filters.text & filters.private)
    ]
