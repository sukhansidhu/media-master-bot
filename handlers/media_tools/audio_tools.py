from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from utils.ffmpeg import (
    extract_audio,
    convert_audio,
    adjust_audio_speed,
    adjust_audio_volume
)
from utils.progress import progress_callback
from utils.db import Database
from utils.buttons import audio_tools_markup, back_button

db = Database()

async def audio_tools_callback(client, callback_query: CallbackQuery):
    """Handle audio tools callback"""
    user_id = callback_query.from_user.id
    message = callback_query.message
    media_message = message.reply_to_message
    
    if not media_message:
        await callback_query.answer("Original message not found!")
        return
    
    action = callback_query.data.split("_")[-1]
    
    if action == "extract":
        # Extract audio from video
        file_path = await media_message.download()
        output_path = f"data/{user_id}_extracted.mp3"
        
        await callback_query.message.edit_text("🔊 Extracting audio...")
        
        try:
            await extract_audio(
                file_path,
                output_path,
                lambda current, total: progress_callback(
                    client,
                    callback_query.message,
                    current,
                    total,
                    "Extracting audio"
                )
            )
            
            # Upload the extracted audio
            await client.send_audio(
                chat_id=user_id,
                audio=output_path,
                caption="✅ Audio extracted successfully!",
                progress=progress_callback
            )
        except Exception as e:
            await callback_query.message.edit_text(f"❌ Error: {e}")
        finally:
            # Clean up files
            os.unlink(file_path)
            os.unlink(output_path)
    
    elif action == "options":
        await callback_query.message.edit_text(
            "🎵 **Audio Tools**\n\n"
            "Select an audio processing option:",
            reply_markup=audio_tools_markup()
        )

def audio_tools_handler():
    return CallbackQueryHandler(audio_tools_callback, filters.regex("^audio_tools_"))
