from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from utils.ffmpeg import generate_screenshots
from utils.progress import progress_callback
from utils.db import Database
from utils.buttons import back_button

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
                lambda current, total: progress_callback(
                    client,
                    callback_query.message,
                    current,
                    total,
                    "Generating screenshots"
                )
            )
            
            # Send the screenshots
            media_group = []
            for i, path in enumerate(screenshot_paths):
                media_group.append(InputMediaPhoto(
                    media=path,
                    caption=f"Screenshot {i+1}" if i == 0 else ""
                ))
            
            await client.send_media_group(
                chat_id=user_id,
                media=media_group
            )
            
            await callback_query.message.reply_text("✅ Screenshots generated successfully!")
        except Exception as e:
            await callback_query.message.edit_text(f"❌ Error: {e}")
        finally:
            # Clean up files
            os.unlink(file_path)
            for path in screenshot_paths:
                os.unlink(path)
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
        screenshot_path = await generate_screenshots(
            file_path,
            output_path,
            timestamps=[timestamp],
            progress_callback=lambda current, total: progress_callback(
                client,
                message,
                current,
                total,
                "Taking screenshot"
            )
        )
        
        # Send the screenshot
        await client.send_photo(
            chat_id=user_id,
            photo=output_path,
            caption=f"✅ Screenshot at {timestamp}"
        )
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
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
        MessageHandler(screenshot_message, filters.text & filters.private & ~filters.command)
      ]
