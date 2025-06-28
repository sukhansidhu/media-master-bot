import os
import asyncio
import ffmpeg
from typing import List, Callable, Optional, Dict
from config import Config

# Global dictionary to track ongoing processes
ongoing_processes = {}

async def run_ffmpeg_command(input_path: str, output_path: str, command: List[str], 
                           task_id: str = None,
                           progress_callback: Optional[Callable] = None) -> bool:
    """Run FFmpeg command with progress tracking"""
    try:
        process = await asyncio.create_subprocess_exec(
            Config.FFMPEG_PATH,
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Store process if task_id is provided
        if task_id:
            ongoing_processes[task_id] = process
        
        # If progress callback is provided, track progress
        if progress_callback:
            while True:
                await asyncio.sleep(1)
                if process.returncode is not None:
                    break
                
                # Get file size for progress calculation
                if os.path.exists(output_path):
                    current_size = os.path.getsize(output_path)
                    total_size = os.path.getsize(input_path)
                    progress_callback(current_size, total_size)
        
        await process.wait()
        return process.returncode == 0
    except Exception as e:
        print(f"FFmpeg error: {e}")
        return False
    finally:
        # Remove process from tracking
        if task_id and task_id in ongoing_processes:
            del ongoing_processes[task_id]

async def cancel_ffmpeg_process(task_id: str) -> bool:
    """Cancel an ongoing FFmpeg process by task ID"""
    if task_id in ongoing_processes:
        process = ongoing_processes[task_id]
        try:
            process.terminate()
            await process.wait()
            return True
        except Exception as e:
            print(f"Error canceling process: {e}")
        finally:
            del ongoing_processes[task_id]
    return False

async def convert_to_streamable(input_path: str, output_path: str, 
                              task_id: str = None,
                              progress_callback: Optional[Callable] = None) -> bool:
    """Convert video to streamable format"""
    command = [
        "-i", input_path,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "22",
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
        output_path
    ]
    return await run_ffmpeg_command(input_path, output_path, command, task_id, progress_callback)

async def trim_video(input_path: str, output_path: str, start_time: str, end_time: str,
                   task_id: str = None,
                   progress_callback: Optional[Callable] = None) -> bool:
    """Trim video between start and end times"""
    command = [
        "-i", input_path,
        "-ss", start_time,
        "-to", end_time,
        "-c", "copy",
        output_path
    ]
    return await run_ffmpeg_command(input_path, output_path, command, task_id, progress_callback)

async def merge_videos(input_paths: List[str], output_path: str,
                     task_id: str = None,
                     progress_callback: Optional[Callable] = None) -> bool:
    """Merge multiple videos into one"""
    # Create input file list
    list_path = f"{output_path}.txt"
    with open(list_path, "w") as f:
        for path in input_paths:
            f.write(f"file '{os.path.abspath(path)}'\n")
    
    command = [
        "-f", "concat",
        "-safe", "0",
        "-i", list_path,
        "-c", "copy",
        output_path
    ]
    
    success = await run_ffmpeg_command(input_paths[0], output_path, command, task_id, progress_callback)
    if os.path.exists(list_path):
        os.unlink(list_path)
    return success

async def extract_audio(input_path: str, output_path: str,
                      task_id: str = None,
                      progress_callback: Optional[Callable] = None) -> bool:
    """Extract audio from video"""
    command = [
        "-i", input_path,
        "-vn",
        "-acodec", "libmp3lame",
        "-ab", "192k",
        output_path
    ]
    return await run_ffmpeg_command(input_path, output_path, command, task_id, progress_callback)

async def generate_screenshots(input_path: str, output_dir: str, count: int = 5,
                            timestamps: Optional[List[str]] = None,
                            task_id: str = None,
                            progress_callback: Optional[Callable] = None) -> List[str]:
    """Generate screenshots from video"""
    if not timestamps:
        # Get video duration
        probe = ffmpeg.probe(input_path)
        duration = float(probe["format"]["duration"])
        
        # Calculate evenly spaced timestamps
        interval = duration / (count + 1)
        timestamps = [interval * (i + 1) for i in range(count)]
    
    output_paths = []
    for i, timestamp in enumerate(timestamps):
        output_path = os.path.join(output_dir, f"screenshot_{i+1}.jpg")
        command = [
            "-i", input_path,
            "-ss", str(timestamp),
            "-vframes", "1",
            "-q:v", "2",
            output_path
        ]
        
        if await run_ffmpeg_command(input_path, output_path, command, task_id, progress_callback):
            output_paths.append(output_path)
    
    return output_paths

async def convert_media(input_path: str, output_path: str, target_format: str,
                      task_id: str = None,
                      progress_callback: Optional[Callable] = None) -> bool:
    """Convert media to different format"""
    command = ["-i", input_path]
    
    # Add format-specific options
    if target_format in ["mp4", "mkv", "avi"]:
        command.extend([
            "-c:v", "libx264",
            "-preset", "fast",
            "-c:a", "aac"
        ])
    elif target_format in ["mp3", "wav", "flac"]:
        command.extend(["-q:a", "0"])
    
    command.append(output_path)
    return await run_ffmpeg_command(input_path, output_path, command, task_id, progress_callback)

async def edit_metadata(input_path: str, output_path: str, metadata: Dict[str, str], 
                      task_id: str = None,
                      progress_callback: Optional[Callable] = None) -> bool:
    """Edit media metadata"""
    command = [
        "-i", input_path,
        "-c", "copy",  # Copy without re-encoding
    ]
    
    for key, value in metadata.items():
        command.extend(["-metadata", f"{key}={value}"])
    
    command.append(output_path)
    
    return await run_ffmpeg_command(input_path, output_path, command, task_id, progress_callback)
