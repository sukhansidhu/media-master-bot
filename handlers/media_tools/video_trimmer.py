import os
from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from utils.ffmpeg import trim_video
from utils.progress import progress_callback
from utils.db import Database
from utils.buttons import back_button

db = Database()

async def video_trimmer_callback(client, callback_query: CallbackQuery):
    """Handle video trimmer callback"""
    user_id = callback_query.from_user.id
    message = callback_query.message
    media_message = message.reply_to_message
    
    if not media_message:
        await callback_query.answer("Original message not found!")
        return
    
    await callback_query.message.edit_text(
        "✂️ **Video Trimmer**\n\n"
        "Send the start and end time in format:\n"
        "`HH:MM:SS HH:MM:SS`\n\n"
        "Example: `00:01:30 00:02:45`\n"
        "This will trim from 1min 30sec to 2min 45sec",
        reply_markup=back_button("media_options")
    )
    
    # Store the media message ID for later reference
    await db.set_temp_data(user_id, "video_trimmer", {
        "media_message_id": media_message.id
    })

async def video_trimmer_message(client, message: Message):
    """Handle video trimmer time input"""
    user_id = message.from_user.id
    temp_data = await db.get_temp_data(user_id, "video_trimmer")
    
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
    
    # Parse time input
    try:
        times = message.text.split()
        if len(times) != 2:
            raise ValueError("Invalid time format")
        
        start_time = times[0]
        end_time = times[1]
        
        # Validate time format
        def validate_time(time_str):
            parts = time_str.split(":")
            if len(parts) != 3:
                raise ValueError("Invalid time format")
            return all(part.isdigit() for part in parts)
        
        if not validate_time(start_time) or not validate_time(end_time):
            raise ValueError("Invalid time format")
        
    except Exception as e:
        await message.reply_text(f"❌ Invalid time format: {e}")
        return
    
    # Download the video
    file_path = await media_message.download()
    output_path = f"data/{user_id}_trimmed.mp4"
    
    await message.reply_text("✂️ Trimming video...")
    
    try:
        await trim_video(
            file_path,
            output_path,
            start_time,
            end_time,
            lambda current, total, progress, elapsed: progress_callback(
                client,
                message,
                current,
                total,
                progress,
                elapsed,
                "Trimming video"
            )
        )
        
        # Upload the trimmed video
        await client.send_video(
            chat_id=user_id,
            video=output_path,
            caption=f"✅ Trimmed video from {start_time} to {end_time}",
            progress=progress_callback
        )
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
    finally:
        # Clean up files
        os.unlink(file_path)
        os.unlink(output_path)
    
    # Clean up temp data
    await db.delete_temp_data(user_id, "video_trimmer")

def video_trimmer_handler():
    return [
        CallbackQueryHandler(video_trimmer_callback, filters.regex("^video_trimmer_")),
        MessageHandler(video_trimmer_message, filters.text & filters.private)
    ]
