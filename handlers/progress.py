import os
from pyrogram import filters
from pyrogram.types import Message, CallbackQuery
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from utils.ffmpeg import cancel_ffmpeg_process
from utils.db import Database

db = Database()

async def cancel_processing(client, callback_query: CallbackQuery):
    """Handle cancel processing request"""
    user_id = callback_query.from_user.id
    task_id = callback_query.data.split("_")[-1]
    
    # Cancel the FFmpeg process
    success = await cancel_ffmpeg_process(user_id, task_id)
    
    if success:
        await callback_query.answer("Processing cancelled!")
        await callback_query.message.edit_text("❌ Processing cancelled by user.")
    else:
        await callback_query.answer("Failed to cancel processing or already completed.")

progress_handler = CallbackQueryHandler(cancel_processing, filters.regex("^cancel_"))
