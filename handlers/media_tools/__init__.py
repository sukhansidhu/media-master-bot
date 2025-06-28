import logging

logger = logging.getLogger(__name__)

# Import all handler functions with error handling
handler_functions = []

try:
    from .caption_editor import caption_editor_handler
    handler_functions.append(caption_editor_handler)
except ImportError as e:
    logger.error(f"Couldn't import caption_editor: {e}")

try:
    from .metadata_editor import metadata_editor_handler
    handler_functions.append(metadata_editor_handler)
except ImportError as e:
    logger.error(f"Couldn't import metadata_editor: {e}")

try:
    from .forwarder import forwarder_handler
    handler_functions.append(forwarder_handler)
except ImportError as e:
    logger.error(f"Couldn't import forwarder: {e}")

try:
    from .stream_tools import stream_tools_handler
    handler_functions.append(stream_tools_handler)
except ImportError as e:
    logger.error(f"Couldn't import stream_tools: {e}")

try:
    from .video_trimmer import video_trimmer_handler
    handler_functions.append(video_trimmer_handler)
except ImportError as e:
    logger.error(f"Couldn't import video_trimmer: {e}")

try:
    from .video_merger import video_merger_handler
    handler_functions.append(video_merger_handler)
except ImportError as e:
    logger.error(f"Couldn't import video_merger: {e}")

try:
    from .audio_tools import audio_tools_handler
    handler_functions.append(audio_tools_handler)
except ImportError as e:
    logger.error(f"Couldn't import audio_tools: {e}")

try:
    from .screenshot import screenshot_handler
    handler_functions.append(screenshot_handler)
except ImportError as e:
    logger.error(f"Couldn't import screenshot: {e}")

try:
    from .converter import converter_handler
    handler_functions.append(converter_handler)
except ImportError as e:
    logger.error(f"Couldn't import converter: {e}")

try:
    from .renamer import renamer_handler
    handler_functions.append(renamer_handler)
except ImportError as e:
    logger.error(f"Couldn't import renamer: {e}")

try:
    from .media_info import media_info_handler
    handler_functions.append(media_info_handler)
except ImportError as e:
    logger.error(f"Couldn't import media_info: {e}")

try:
    from .archiver import archiver_handler
    handler_functions.append(archiver_handler)
except ImportError as e:
    logger.error(f"Couldn't import archiver: {e}")

# Create a flat list of all handlers
media_handlers = []

# Helper function to add handlers safely
def add_handler(handler_func):
    if handler_func is None:
        return
    
    try:
        result = handler_func()
        
        # If it's a single handler, wrap it in a list
        if not isinstance(result, list):
            result = [result]
            
        media_handlers.extend(result)
        logger.info(f"Added {len(result)} handlers from {handler_func.__name__}")
    except Exception as e:
        logger.error(f"Error in handler function {handler_func.__name__}: {e}")

# Add all handlers using the safe method
for handler_func in handler_functions:
    add_handler(handler_func)

logger.info(f"Total media handlers loaded: {len(media_handlers)}")
