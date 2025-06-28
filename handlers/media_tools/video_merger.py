import os
from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from utils.ffmpeg import merge_videos
from utils.progress import progress_callback
from utils.db import Database
from utils.buttons import back_button

db = Database()

async def video_merger_callback(client, callback_query: CallbackQuery):
    """Handle video merger callback"""
    user_id = callback_query.from_user.id
    message = callback_query.message
    media_message = message.reply_to_message
    
    if not media_message:
        await callback_query.answer("Original message not found!")
        return
    
    await callback_query.message.edit_text(
        "🎞️ **Video Merger**\n\n"
        "Send me another video to merge with this one.\n"
        "The videos will be merged in the order you send them.",
        reply_markup=back_button("media_options")
    )
    
    # Store the first video info
    file_path = await media_message.download()
    temp_path = f"data/{user_id}_video1.mp4"
    os.rename(file_path, temp_path)
    
    await db.set_temp_data(user_id, "video_merger", {
        "video1_path": temp_path
    })

async def video_merger_message(client, message: Message):
    """Handle second video for merging"""
    user_id = message.from_user.id
    temp_data = await db.get_temp_data(user_id, "video_merger")
    
    if not temp_data or not message.video:
        return
    
    video1_path = temp_data.get("video1_path")
    video2_path = await message.download()
    output_path = f"data/{user_id}_merged.mp4"
    
    await message.reply_text("🔄 Merging videos...")
    
    try:
        await merge_videos(
            [video1_path, video2_path],
            output_path,
            lambda current, total, progress, elapsed: progress_callback(
                client,
                message,
                current,
                total,
                progress,
                elapsed,
                "Merging videos"
            )
        )
        
        # Upload the merged video
        await client.send_video(
            chat_id=user_id,
            video=output_path,
            caption="✅ Videos merged successfully!",
            progress=progress_callback
        )
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
    finally:
        # Clean up files
        if os.path.exists(video1_path):
            os.unlink(video1_path)
        if os.path.exists(video2_path):
            os.unlink(video2_path)
        if os.path.exists(output_path):
            os.unlink(output_path)
    
    # Clean up temp data
    await db.delete_temp_data(user_id, "video_merger")

def video_merger_handler():
    return [
        CallbackQueryHandler(video_merger_callback, filters.regex("^video_merger_")),
        MessageHandler(video_merger_message, filters.video & filters.private)
    ]
