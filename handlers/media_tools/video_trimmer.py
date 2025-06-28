    ]
import os
import re
import logging
from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from utils.ffmpeg import trim_video
from utils.progress import progress_callback
from utils.db import Database
from utils.buttons import back_button

logger = logging.getLogger(__name__)
db = Database()


async def video_trimmer_callback(client, callback_query: CallbackQuery):
    """Handle video trimmer callback"""
    try:
        user_id = callback_query.from_user.id
        message = callback_query.message
        media_message = message.reply_to_message

        if not media_message or not media_message.video:
            await callback_query.answer("Original video message not found!")
            return

        await callback_query.message.edit_text(
            "✂️ **Video Trimmer**\n\n"
            "Send the start and end time in format:\n"
            "`HH:MM:SS HH:MM:SS`\n\n"
            "Example: `00:01:30 00:02:45`\n"
            "This will trim from 1min 30sec to 2min 45sec",
            reply_markup=back_button("back_to_media")
        )

        await db.set_temp_data(user_id, "video_trimmer", {
            "media_message_id": media_message.id,
            "chat_id": message.chat.id
        })
        await callback_query.answer()

    except Exception as e:
        logger.error(f"Error in video_trimmer_callback: {e}")
        await callback_query.answer("❌ An error occurred", show_alert=True)


async def video_trimmer_message(client, message: Message):
    """Handle video trimmer time input"""
    try:
        user_id = message.from_user.id
        temp_data = await db.get_temp_data(user_id, "video_trimmer")

        if not temp_data:
            return

        # Skip command messages
        if message.text.startswith('/'):
            return

        # Parse and validate time input
        time_pattern = r"^([01]?\d|2[0-3]):([0-5]?\d):([0-5]?\d)$"
        times = message.text.strip().split()

        if len(times) != 2:
            raise ValueError("Please send exactly 2 time values (start and end)")

        start_time, end_time = times
        if not re.match(time_pattern, start_time) or not re.match(time_pattern, end_time):
            raise ValueError("Invalid time format. Use HH:MM:SS")

        # Get the original video message
        media_message = await client.get_messages(
            temp_data["chat_id"],
            temp_data["media_message_id"]
        )

        if not media_message or not media_message.video:
            raise ValueError("Original video message not found")

        # Download the video
        file_path = await media_message.download()
        output_path = f"data/{user_id}_trimmed_{os.path.basename(file_path)}"

        processing_msg = await message.reply_text("✂️ Trimming video...")

        try:
            await trim_video(
                file_path,
                output_path,
                start_time,
                end_time,
                lambda current, total, progress, elapsed: progress_callback(
                    client,
                    processing_msg,
                    current,
                    total,
                    progress,
                    elapsed,
                    "Trimming video"
                )
            )

            # Upload the trimmed video
            await client.send_video(
                chat_id=message.chat.id,
                video=output_path,
                caption=f"✅ Trimmed from {start_time} to {end_time}",
                reply_to_message_id=message.id,
                progress=progress_callback
            )

        finally:
            # Clean up files
            for path in [file_path, output_path]:
                if os.path.exists(path):
                    try:
                        os.unlink(path)
                    except Exception as e:
                        logger.error(f"Error deleting file {path}: {e}")

        await processing_msg.delete()

    except Exception as e:
        logger.error(f"Error in video_trimmer_message: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")

    finally:
        await db.delete_temp_data(user_id, "video_trimmer")


def video_trimmer_handler():
    """Return video trimmer handlers"""
    return [
        CallbackQueryHandler(video_trimmer_callback, filters.regex(r"^trim_video$")),
        MessageHandler(
            filters.text & filters.private & (~filters.regex(r"^/")),
            video_trimmer_message
        )
        ]
