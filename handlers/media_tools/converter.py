from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from utils.ffmpeg import convert_media
from utils.progress import progress_callback
from utils.db import Database
from utils.buttons import format_markup, back_button

db = Database()

async def converter_callback(client, callback_query: CallbackQuery):
    """Handle converter callback"""
    user_id = callback_query.from_user.id
    message = callback_query.message
    media_message = message.reply_to_message
    
    if not media_message:
        await callback_query.answer("Original message not found!")
        return
    
    action = callback_query.data.split("_")[-1]
    
    if action == "options":
        await callback_query.message.edit_text(
            "🔄 **Media Converter**\n\n"
            "Select target format:",
            reply_markup=format_markup(media_message)
        )
    
    elif action.startswith("format_"):
        target_format = action.split("_")[-1]
        
        # Download the original file
        file_path = await media_message.download()
        output_path = f"data/{user_id}_converted.{target_format}"
        
        await callback_query.message.edit_text(f"🔄 Converting to {target_format.upper()}...")
        
        try:
            await convert_media(
                file_path,
                output_path,
                target_format,
                lambda current, total: progress_callback(
                    client,
                    callback_query.message,
                    current,
                    total,
                    f"Converting to {target_format.upper()}"
                )
            )
            
            # Send the converted file
            if target_format in ["mp4", "mkv", "avi"]:
                await client.send_video(
                    chat_id=user_id,
                    video=output_path,
                    caption=f"✅ Converted to {target_format.upper()}",
                    progress=progress_callback
                )
            elif target_format in ["mp3", "wav", "flac"]:
                await client.send_audio(
                    chat_id=user_id,
                    audio=output_path,
                    caption=f"✅ Converted to {target_format.upper()}",
                    progress=progress_callback
                )
            else:
                await client.send_document(
                    chat_id=user_id,
                    document=output_path,
                    caption=f"✅ Converted to {target_format.upper()}",
                    progress=progress_callback
                )
        except Exception as e:
            await callback_query.message.edit_text(f"❌ Error: {e}")
        finally:
            # Clean up files
            os.unlink(file_path)
            os.unlink(output_path)

def converter_handler():
    return CallbackQueryHandler(converter_callback, filters.regex("^converter_"))
