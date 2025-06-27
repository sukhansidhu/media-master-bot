from pyrogram import filters
from pyrogram.types import CallbackQuery
from pyrogram.handlers import CallbackQueryHandler
from utils.ffmpeg import convert_to_streamable
from utils.progress import progress_callback

async def stream_tools_callback(client, callback_query: CallbackQuery):
    """Handle stream tools callback"""
    user_id = callback_query.from_user.id
    message = callback_query.message
    media_message = message.reply_to_message
    
    if not media_message:
        await callback_query.answer("Original message not found!")
        return
    
    # Download the media file
    file_path = await media_message.download()
    
    # Convert to streamable format
    output_path = f"data/{user_id}_streamable.mp4"
    
    await callback_query.message.edit_text("🔄 Converting to streamable format...")
    
    try:
        await convert_to_streamable(
            file_path,
            output_path,
            lambda current, total: progress_callback(
                client,
                callback_query.message,
                current,
                total,
                "Converting to streamable"
            )
        )
        
        # Upload the converted file
        await client.send_video(
            chat_id=user_id,
            video=output_path,
            caption="✅ Converted to streamable format",
            progress=progress_callback
        )
    except Exception as e:
        await callback_query.message.edit_text(f"❌ Error: {e}")
    finally:
        # Clean up files
        os.unlink(file_path)
        os.unlink(output_path)

def stream_tools_handler():
    return CallbackQueryHandler(stream_tools_callback, filters.regex("^stream_tools_"))
