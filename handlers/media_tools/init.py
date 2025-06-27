from .caption_editor import caption_editor_handler
from .metadata_editor import metadata_editor_handler
from .forwarder import forwarder_handler
from .stream_tools import stream_tools_handler
from .video_trimmer import video_trimmer_handler
from .video_merger import video_merger_handler
from .audio_tools import audio_tools_handler
from .screenshot import screenshot_handler
from .converter import converter_handler
from .renamer import renamer_handler
from .media_info import media_info_handler
from .archiver import archiver_handler

def media_tools_handlers():
    """Return all media tools handlers as a flat list"""
    handlers = []
    handlers.extend(caption_editor_handler())
    handlers.extend(metadata_editor_handler())
    handlers.extend(forwarder_handler())
    handlers.extend(stream_tools_handler())
    handlers.extend(video_trimmer_handler())
    handlers.extend(video_merger_handler())
    handlers.extend(audio_tools_handler())
    handlers.extend(screenshot_handler())
    handlers.extend(converter_handler())
    handlers.extend(renamer_handler())
    handlers.extend(media_info_handler())
    handlers.extend(archiver_handler())
    return handlers
