"""Module to delete media files"""
import os
import shutil
from config import SCREENSHOT_FILE_PATH, AUDIO_FILE_PATH, VIDEO_FILE_PATH


def delete_screenshots():
    """Delete all files and folders inside screenshot filepath"""
    for filename in os.listdir(SCREENSHOT_FILE_PATH):
        file_path = os.path.join(SCREENSHOT_FILE_PATH, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


def delete_audio_file():
    """Delete audio file"""
    try:
        os.unlink(AUDIO_FILE_PATH)
    except Exception as e:
        print(f"Failed to delete {AUDIO_FILE_PATH}. Reason: {e}")


def delete_video_file():
    """Delete video file"""
    try:
        os.unlink(VIDEO_FILE_PATH)
    except Exception as e:
        print(f"Failed to delete {VIDEO_FILE_PATH}. Reason: {e}")
