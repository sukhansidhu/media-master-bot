from pyrogram.types import Message
from config import Config
import time

async def progress_callback(client: Client, message: Message, current: int, total: int, action: str):
    """Progress callback for uploads and processing"""
    # Calculate percentage
    percentage = (current / total) * 100
    
    # Update message every 5% or 5 seconds
    now = time.time()
    last_update = getattr(progress_callback, "last_update", 0)
    
    if percentage == 100 or now - last_update >= 5 or percentage - getattr(progress_callback, "last_percentage", 0) >= 5:
        try:
            await message.edit_text(
                f"🔄 **{action}**\n\n"
                f"Progress: {percentage:.1f}%\n"
                f"`{human_readable_size(current)} / {human_readable_size(total)}`"
            )
        except:
            pass
        
        progress_callback.last_update = now
        progress_callback.last_percentage = percentage

def human_readable_size(size: int) -> str:
    """Convert bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"
