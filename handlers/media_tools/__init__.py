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

# Create a flat list of all handlers
media_handlers = []

# Wrap each handler function call in a list
media_handlers.extend([caption_editor_handler()])
media_handlers.extend([metadata_editor_handler()])
media_handlers.extend([forwarder_handler()])
media_handlers.extend([stream_tools_handler()])
media_handlers.extend([video_trimmer_handler()])
media_handlers.extend([video_merger_handler()])
media_handlers.extend([audio_tools_handler()])
media_handlers.extend([screenshot_handler()])
media_handlers.extend([converter_handler()])
media_handlers.extend([renamer_handler()])
media_handlers.extend([media_info_handler()])
media_handlers.extend([archiver_handler()])
