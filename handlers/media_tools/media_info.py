from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.handlers import CallbackQueryHandler
import ffmpeg
import os
import logging
from utils.buttons import back_button

logger = logging.getLogger(__name__)

async def media_info_callback(client, callback_query: CallbackQuery):
    """Handle media info callback"""
    try:
        message = callback_query.message
        media_message = message.reply_to_message
        
        if not media_message:
            await callback_query.answer("Original message not found!")
            return
        
        # Download the file
        file_path = await media_message.download()
        
        try:
            # Get media info using ffmpeg
            probe = ffmpeg.probe(file_path)
            format_info = probe.get("format", {})
            streams = probe.get("streams", [])
            
            # Prepare info text
            info_text = "📊 **Media Information**\n\n"
            info_text += f"📝 **File Name:** `{os.path.basename(file_path)}`\n"
            info_text += f"📦 **Format:** `{format_info.get('format_name', 'N/A')}`\n"
            info_text += f"⏱️ **Duration:** `{float(format_info.get('duration', 0)):.2f}s`\n"
            info_text += f"📏 **Size:** `{int(format_info.get('size', 0)):,} bytes`\n\n"
            
            # Add stream info
            for i, stream in enumerate(streams):
                info_text += f"📡 **Stream {i+1}**\n"
                info_text += f"• **Type:** `{stream.get('codec_type', 'N/A')}`\n"
                info_text += f"• **Codec:** `{stream.get('codec_name', 'N/A')}`\n"
                
                if stream.get("codec_type") == "video":
                    info_text += f"• **Resolution:** `{stream.get('width', 'N/A')}x{stream.get('height', 'N/A')}`\n"
                    info_text += f"• **FPS:** `{stream.get('r_frame_rate', 'N/A')}`\n"
                elif stream.get("codec_type") == "audio":
                    info_text += f"• **Sample Rate:** `{stream.get('sample_rate', 'N/A')} Hz`\n"
                    info_text += f"• **Channels:** `{stream.get('channels', 'N/A')}`\n"
                    info_text += f"• **Bitrate:** `{int(stream.get('bit_rate', 0)):,}`\n"
                
                info_text += "\n"
            
            await callback_query.message.edit_text(
                info_text,
                reply_markup=InlineKeyboardMarkup([
                    [back_button("media_options")]
                ])
            )
        except Exception as e:
            await callback_query.message.edit_text(
                f"❌ Error getting media info: {str(e)}",
                reply_markup=InlineKeyboardMarkup([
                    [back_button("media_options")]
                ])
            )
            logger.error(f"Media info error: {e}")
        finally:
            # Clean up file
            if os.path.exists(file_path):
                os.unlink(file_path)
    except Exception as e:
        await callback_query.answer(f"Error: {e}", show_alert=True)
        logger.error(f"Media info callback error: {e}")
        raise

def media_info_handler():
    """Return list of media info handlers"""
    return [
        CallbackQueryHandler(media_info_callback, filters.regex(r"^media_info_"))
                ]
