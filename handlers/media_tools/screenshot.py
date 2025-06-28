import os
import logging
from pyrogram import filters
from pyrogram.types import CallbackQuery, Message, InputMediaPhoto
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from utils.ffmpeg import generate_screenshots
from utils.progress import progress_callback
from utils.db import Database
from utils.buttons import back_button

logger = logging.getLogger(__name__)
db = Database()

async def screenshot_callback(client, callback_query: CallbackQuery):
    """Handle screenshot callback"""
    user_id = callback_query.from_user.id
    message = callback_query.message
    media_message = message.reply_to_message
    
    if not media_message:
        await callback_query.answer("Original message not found!")
        return
    
    action = callback_query.data.split("_")[-1]
    
    if action == "auto":
        # Generate automatic screenshots
        file_path = await media_message.download()
        output_dir = f"data/{user_id}_screenshots"
        os.makedirs(output_dir, exist_ok=True)
        
        await callback_query.message.edit_text("📸 Generating screenshots...")
        
        try:
            screenshot_paths = await generate_screenshots(
                file_path,
                output_dir,
                count=5,  # Generate 5 screenshots
                progress_callback=lambda current, total, progress, elapsed: progress_callback(
                    client,
                    callback_query.message,
                    current,
                    total,
                    progress,
                    elapsed,
                    "Generating screenshots"
                )
            )
            
            # Send the screenshots
            media_group = []
            for i, path in enumerate(screenshot_paths):
                if i == 0:
                    media_group.append(InputMediaPhoto(
                        media=path,
                        caption="✅ Screenshots generated"
                    ))
                else:
                    media_group.append(InputMediaPhoto(media=path))
            
            await client.send_media_group(
                chat_id=user_id,
                media=media_group
            )
            
            await callback_query.message.delete()
        except Exception as e:
            logger.error(f"Screenshot error: {e}")
            await callback_query.message.edit_text(f"❌ Error: {str(e)}")
        finally:
            # Clean up files
            if os.path.exists(file_path):
                os.unlink(file_path)
            for path in screenshot_paths:
                if os.path.exists(path):
                    os.unlink(path)
            if os.path.exists(output_dir):
                os.rmdir(output_dir)
    
    elif action == "manual":
        await callback_query.message.edit_text(
            "⏱️ **Manual Screenshot**\n\n"
            "Send the timestamp (HH:MM:SS) where you want to take the screenshot:",
            reply_markup=back_button("media_options")
        )
        
        # Store the media message ID for later reference
        await db.set_temp_data(user_id, "screenshot_manual", {
            "media_message_id": media_message.id
        })

async def screenshot_message(client, message: Message):
    """Handle manual screenshot timestamp input"""
    user_id = message.from_user.id
    temp_data = await db.get_temp_data(user_id, "screenshot_manual")
    
    if not temp_data:
        return
    
    media_message_id = temp_data.get("media_message_id")
    media_message = await client.get_messages(message.chat.id, media_message_id)
    
    if not media_message:
        await message.reply_text("Original media message not found!")
        return
    
    # Validate timestamp
    try:
        timestamp = message.text
        parts = timestamp.split(":")
        if len(parts) != 3:
            raise ValueError("Invalid timestamp format")
        
        # Download the video
        file_path = await media_message.download()
        output_path = f"data/{user_id}_screenshot.jpg"
        
        await message.reply_text("📸 Taking screenshot...")
        
        # Generate screenshot at specific timestamp
        screenshot_paths = await generate_screenshots(
            file_path,
            output_path,
            timestamps=[timestamp],
            progress_callback=lambda current, total, progress, elapsed: progress_callback(
                client,
                message,
                current,
                total,
                progress,
                elapsed,
                "Taking screenshot"
            )
        )
        
        if screenshot_paths:
            # Send the screenshot
            await client.send_photo(
                chat_id=user_id,
                photo=screenshot_paths[0],
                caption=f"✅ Screenshot at {timestamp}"
            )
        else:
            await message.reply_text("❌ Failed to generate screenshot")
    except Exception as e:
        logger.error(f"Manual screenshot error: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")
    finally:
        # Clean up files
        if os.path.exists(file_path):
            os.unlink(file_path)
        if os.path.exists(output_path):
            os.unlink(output_path)
    
    # Clean up temp data
    await db.delete_temp_data(user_id, "screenshot_manual")

def screenshot_handler():
    return [
        CallbackQueryHandler(screenshot_callback, filters.regex("^screenshot_")),
        MessageHandler(screenshot_message, filters.text & filters.private)
    ]
