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

# Create a list of all handler functions
media_handlers = [
    caption_editor_handler(),
    metadata_editor_handler(),
    forwarder_handler(),
    stream_tools_handler(),
    video_trimmer_handler(),
    video_merger_handler(),
    audio_tools_handler(),
    screenshot_handler(),
    converter_handler(),
    renamer_handler(),
    media_info_handler(),
    archiver_handler()
]
