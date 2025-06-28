from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_markup():
    """Start command buttons"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 Help", callback_data="help")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="settings")]
    ])

def settings_markup():
    """Settings command buttons"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📤 Upload Mode", callback_data="settings_upload_mode"),
            InlineKeyboardButton("🔄 Auto Rename", callback_data="settings_auto_rename")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="start_back")]
    ])

def get_media_options(message, is_premium=False):
    """Get appropriate buttons based on media type"""
    buttons = []
    
    if message.video:
        buttons.extend([
            [InlineKeyboardButton("✂️ Trim Video", callback_data="video_trimmer_options")],
            [InlineKeyboardButton("🎞️ Merge Videos", callback_data="video_merger_options")],
            [InlineKeyboardButton("🔊 Extract Audio", callback_data="audio_tools_extract")],
            [InlineKeyboardButton("📸 Screenshots", callback_data="screenshot_options")],
            [InlineKeyboardButton("🔄 Convert Format", callback_data="converter_options")]
        ])
    elif message.audio:
        buttons.extend([
            [InlineKeyboardButton("🎵 Audio Tools", callback_data="audio_tools_options")],
            [InlineKeyboardButton("🔄 Convert Format", callback_data="converter_options")]
        ])
    elif message.document:
        buttons.extend([
            [InlineKeyboardButton("📝 Rename File", callback_data="renamer_options")],
            [InlineKeyboardButton("🗄️ Create Archive", callback_data="archiver_options")]
        ])
    
    # Common buttons for all media types
    common_buttons = [
        [InlineKeyboardButton("✏️ Edit Caption", callback_data="caption_editor_options")],
        [InlineKeyboardButton("📊 Media Info", callback_data="media_info_options")],
        [InlineKeyboardButton("🗄️ Create Archive", callback_data="archiver_options")]
    ]
    
    # Only show Rename button if not already shown for documents
    if not message.document:
        common_buttons.insert(0, [InlineKeyboardButton("📝 Rename File", callback_data="renamer_options")])
    
    buttons.extend(common_buttons)
    
    return buttons

def back_button(target):
    """Back button"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data=target)]
    ])

def audio_tools_markup():
    """Audio tools buttons"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎚️ Volume", callback_data="audio_volume"),
            InlineKeyboardButton("⏩ Speed", callback_data="audio_speed")
        ],
        [
            InlineKeyboardButton("🎛️ Equalizer", callback_data="audio_equalizer"),
            InlineKeyboardButton("🔊 Bass Boost", callback_data="audio_bass")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="media_options")]
    ])

def format_markup(message):
    """Format conversion buttons"""
    buttons = []
    
    if message.video:
        buttons.append([InlineKeyboardButton("MP4", callback_data="converter_format_mp4")])
        buttons.append([InlineKeyboardButton("MKV", callback_data="converter_format_mkv")])
        buttons.append([InlineKeyboardButton("AVI", callback_data="converter_format_avi")])
        buttons.append([InlineKeyboardButton("GIF", callback_data="converter_format_gif")])
    elif message.audio:
        buttons.append([InlineKeyboardButton("MP3", callback_data="converter_format_mp3")])
        buttons.append([InlineKeyboardButton("WAV", callback_data="converter_format_wav")])
        buttons.append([InlineKeyboardButton("FLAC", callback_data="converter_format_flac")])
    elif message.document:
        buttons.append([InlineKeyboardButton("PDF", callback_data="converter_format_pdf")])
        buttons.append([InlineKeyboardButton("DOCX", callback_data="converter_format_docx")])
    
    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="media_options")])
    return InlineKeyboardMarkup(buttons)

def archive_markup():
    """Archive format buttons"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("ZIP", callback_data="archiver_format_zip")],
        [InlineKeyboardButton("RAR (Password)", callback_data="archive_password_rar")],
        [InlineKeyboardButton("7Z (Password)", callback_data="archive_password_7z")],
        [InlineKeyboardButton("🔙 Back", callback_data="media_options")]
    ])
