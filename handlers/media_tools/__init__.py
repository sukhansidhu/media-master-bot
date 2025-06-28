import logging
import traceback
from pyrogram.handlers import CallbackQueryHandler, MessageHandler

logger = logging.getLogger(__name__)

def safe_extend_handler(handler_func, handler_list):
    """Safely extend handler list with a handler function's output"""
    try:
        if handler_func is None:
            return

        result = handler_func()

        if result is None:
            return
        elif isinstance(result, (CallbackQueryHandler, MessageHandler)):
            handler_list.append(result)
        elif isinstance(result, list):
            handler_list.extend(result)
        else:
            logger.error(f"Invalid handler type from {handler_func.__module__}: {type(result)}")
    except Exception as e:
        logger.error(f"Error in {handler_func.__module__}: {e}")
        logger.error(traceback.format_exc())

# Initialize media handlers list
media_handlers = []

try:
    from .caption_editor import caption_editor_handler
    safe_extend_handler(caption_editor_handler, media_handlers)
except ImportError as e:
    logger.error(f"Couldn't import caption_editor: {e}")
    logger.error(traceback.format_exc())

try:
    from .metadata_editor import metadata_editor_handler
    safe_extend_handler(metadata_editor_handler, media_handlers)
except ImportError as e:
    logger.error(f"Couldn't import metadata_editor: {e}")
    logger.error(traceback.format_exc())

try:
    from .forwarder import forwarder_handler
    safe_extend_handler(forwarder_handler, media_handlers)
except ImportError as e:
    logger.error(f"Couldn't import forwarder: {e}")
    logger.error(traceback.format_exc())

try:
    from .stream_tools import stream_tools_handler
    safe_extend_handler(stream_tools_handler, media_handlers)
except ImportError as e:
    logger.error(f"Couldn't import stream_tools: {e}")
    logger.error(traceback.format_exc())

try:
    from .video_trimmer import video_trimmer_handler
    safe_extend_handler(video_trimmer_handler, media_handlers)
except ImportError as e:
    logger.error(f"Couldn't import video_trimmer: {e}")
    logger.error(traceback.format_exc())

try:
    from .video_merger import video_merger_handler
    safe_extend_handler(video_merger_handler, media_handlers)
except ImportError as e:
    logger.error(f"Couldn't import video_merger: {e}")
    logger.error(traceback.format_exc())

try:
    from .audio_tools import audio_tools_handler
    safe_extend_handler(audio_tools_handler, media_handlers)
except ImportError as e:
    logger.error(f"Couldn't import audio_tools: {e}")
    logger.error(traceback.format_exc())

try:
    from .screenshot import screenshot_handler
    safe_extend_handler(screenshot_handler, media_handlers)
except ImportError as e:
    logger.error(f"Couldn't import screenshot: {e}")
    logger.error(traceback.format_exc())

try:
    from .converter import converter_handler
    safe_extend_handler(converter_handler, media_handlers)
except ImportError as e:
    logger.error(f"Couldn't import converter: {e}")
    logger.error(traceback.format_exc())

try:
    from .renamer import renamer_handler
    safe_extend_handler(renamer_handler, media_handlers)
except ImportError as e:
    logger.error(f"Couldn't import renamer: {e}")
    logger.error(traceback.format_exc())

try:
    from .media_info import media_info_handler
    safe_extend_handler(media_info_handler, media_handlers)
except ImportError as e:
    logger.error(f"Couldn't import media_info: {e}")
    logger.error(traceback.format_exc())

try:
    from .archiver import archiver_handler
    safe_extend_handler(archiver_handler, media_handlers)
except ImportError as e:
    logger.error(f"Couldn't import archiver: {e}")
    logger.error(traceback.format_exc())

logger.info(f"Total media handlers loaded: {len(media_handlers)}")

__all__ = ['media_handlers']
