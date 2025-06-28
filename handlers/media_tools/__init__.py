import logging

logger = logging.getLogger(__name__)

# Import handler functions
try:
    from .caption_editor import caption_editor_handler
except ImportError as e:
    logger.error(f"Couldn't import caption_editor: {e}")
    caption_editor_handler = None

try:
    from .metadata_editor import metadata_editor_handler
except ImportError as e:
    logger.error(f"Couldn't import metadata_editor: {e}")
    metadata_editor_handler = None

# Repeat this pattern for all other handlers...

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
    except Exception as e:
        logger.error(f"Error in handler function: {e}")

# Add all handlers using the safe method
add_handler(caption_editor_handler)
add_handler(metadata_editor_handler)
add_handler(forwarder_handler)
add_handler(stream_tools_handler)
add_handler(video_trimmer_handler)
add_handler(video_merger_handler)
add_handler(audio_tools_handler)
add_handler(screenshot_handler)
add_handler(converter_handler)
add_handler(renamer_handler)
add_handler(media_info_handler)
add_handler(archiver_handler)

logger.info(f"Total media handlers loaded: {len(media_handlers)}")
