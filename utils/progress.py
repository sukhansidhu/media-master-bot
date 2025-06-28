from pyrogram import Client
from pyrogram.types import Message
import time

def human_readable_size(size: int) -> str:
    """Convert bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"

async def progress_callback(client: Client, message: Message, current: int, total: int, 
                          progress: int, elapsed: float, action: str):
    """Progress callback for uploads and processing"""
    # Update message every 5% or 5 seconds
    now = time.time()
    last_update = getattr(progress_callback, "last_update", 0)
    
    if progress == 100 or now - last_update >= 5 or progress - getattr(progress_callback, "last_progress", 0) >= 5:
        try:
            # Calculate ETA
            if progress > 0 and elapsed > 0:
                total_time = (elapsed * 100) / progress
                eta = total_time - elapsed
                eta_str = f"ETA: {int(eta)}s"
            else:
                eta_str = "Calculating..."
            
            await message.edit_text(
                f"🔄 **{action}**\n\n"
                f"Progress: {progress}%\n"
                f"`{human_readable_size(current)} / {human_readable_size(total)}`\n"
                f"{eta_str}"
            )
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Progress update error: {e}")
        
        progress_callback.last_update = now
        progress_callback.last_progress = progress
