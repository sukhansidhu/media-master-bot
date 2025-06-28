import logging

logger = logging.getLogger(__name__)

# Import handler functions with error handling
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

# Repeat for all other imports...

# Create a flat list of all handlers
media_handlers = []

if caption_editor_handler:
    try:
        media_handlers.extend(caption_editor_handler())
    except Exception as e:
        logger.error(f"Error in caption_editor_handler: {e}")

if metadata_editor_handler:
    try:
        media_handlers.extend(metadata_editor_handler())
    except Exception as e:
        logger.error(f"Error in metadata_editor_handler: {e}")

# Repeat for all other handlers...
