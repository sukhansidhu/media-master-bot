import logging
import traceback

logger = logging.getLogger(__name__)

# Create an empty list for media handlers
media_handlers = []

# Import handler functions with error handling
try:
    from .caption_editor import caption_editor_handler
    media_handlers.extend(caption_editor_handler())
    logger.info("Imported caption_editor_handler")
except ImportError as e:
    logger.error(f"Couldn't import caption_editor: {e}")
except Exception as e:
    logger.error(f"Error in caption_editor_handler: {e}")
    logger.error(traceback.format_exc())

try:
    from .metadata_editor import metadata_editor_handler
    media_handlers.extend(metadata_editor_handler())
    logger.info("Imported metadata_editor_handler")
except ImportError as e:
    logger.error(f"Couldn't import metadata_editor: {e}")
except Exception as e:
    logger.error(f"Error in metadata_editor_handler: {e}")
    logger.error(traceback.format_exc())

try:
    from .forwarder import forwarder_handler
    media_handlers.extend(forwarder_handler())
    logger.info("Imported forwarder_handler")
except ImportError as e:
    logger.error(f"Couldn't import forwarder: {e}")
except Exception as e:
    logger.error(f"Error in forwarder_handler: {e}")
    logger.error(traceback.format_exc())

try:
    from .stream_tools import stream_tools_handler
    media_handlers.extend(stream_tools_handler())
    logger.info("Imported stream_tools_handler")
except ImportError as e:
    logger.error(f"Couldn't import stream_tools: {e}")
except Exception as e:
    logger.error(f"Error in stream_tools_handler: {e}")
    logger.error(traceback.format_exc())

try:
    from .video_trimmer import video_trimmer_handler
    media_handlers.extend(video_trimmer_handler())
    logger.info("Imported video_trimmer_handler")
except ImportError as e:
    logger.error(f"Couldn't import video_trimmer: {e}")
except Exception as e:
    logger.error(f"Error in video_trimmer_handler: {e}")
    logger.error(traceback.format_exc())

try:
    from .video_merger import video_merger_handler
    media_handlers.extend(video_merger_handler())
    logger.info("Imported video_merger_handler")
except ImportError as e:
    logger.error(f"Couldn't import video_merger: {e}")
except Exception as e:
    logger.error(f"Error in video_merger_handler: {e}")
    logger.error(traceback.format_exc())

try:
    from .audio_tools import audio_tools_handler
    media_handlers.extend(audio_tools_handler())
    logger.info("Imported audio_tools_handler")
except ImportError as e:
    logger.error(f"Couldn't import audio_tools: {e}")
except Exception as e:
    logger.error(f"Error in audio_tools_handler: {e}")
    logger.error(traceback.format_exc())

try:
    from .screenshot import screenshot_handler
    media_handlers.extend(screenshot_handler())
    logger.info("Imported screenshot_handler")
except ImportError as e:
    logger.error(f"Couldn't import screenshot: {e}")
except Exception as e:
    logger.error(f"Error in screenshot_handler: {e}")
    logger.error(traceback.format_exc())

try:
    from .converter import converter_handler
    media_handlers.extend(converter_handler())
    logger.info("Imported converter_handler")
except ImportError as e:
    logger.error(f"Couldn't import converter: {e}")
except Exception as e:
    logger.error(f"Error in converter_handler: {e}")
    logger.error(traceback.format_exc())

try:
    from .renamer import renamer_handler
    media_handlers.extend(renamer_handler())
    logger.info("Imported renamer_handler")
except ImportError as e:
    logger.error(f"Couldn't import renamer: {e}")
except Exception as e:
    logger.error(f"Error in renamer_handler: {e}")
    logger.error(traceback.format_exc())

try:
    from .media_info import media_info_handler
    media_handlers.extend(media_info_handler())
    logger.info("Imported media_info_handler")
except ImportError as e:
    logger.error(f"Couldn't import media_info: {e}")
except Exception as e:
    logger.error(f"Error in media_info_handler: {e}")
    logger.error(traceback.format_exc())

try:
    from .archiver import archiver_handler
    media_handlers.extend(archiver_handler())
    logger.info("Imported archiver_handler")
except ImportError as e:
    logger.error(f"Couldn't import archiver: {e}")
except Exception as e:
    logger.error(f"Error in archiver_handler: {e}")
    logger.error(traceback.format_exc())

logger.info(f"Total media handlers loaded: {len(media_handlers)}")

# Export the media_handlers list
__all__ = ['media_handlers']
