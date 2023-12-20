"""Module to generate video"""
import os
import re
from glob import glob
from moviepy.editor import ImageSequenceClip, AudioFileClip
from config import SCREENSHOT_FILE_PATH, AUDIO_FILE_PATH, VIDEO_FILE_PATH


def numerical_sort(value):
    """This function extracts numeric parts from a string"""
    parts = re.split(r"(\d+)", value)
    return [int(part) if part.isdigit() else part for part in parts]


def create_video():
    """Create video using audio and screenshots"""
    # File paths
    image_folder = SCREENSHOT_FILE_PATH
    audio_file = AUDIO_FILE_PATH
    output_file = VIDEO_FILE_PATH

    # Set audio for the video
    audio_clip = AudioFileClip(audio_file)

    # Numerically sort filenames
    filenames = glob(os.path.join(image_folder, "*.png"))
    sorted_filenames = sorted(filenames, key=numerical_sort)

    # Create video clip from image sequence
    sequence_clip = ImageSequenceClip(sorted_filenames, fps=30)
    video_clip = sequence_clip.set_audio(audio_clip)
    video_clip.duration = audio_clip.duration
    video_clip.fps = 60

    # Write the video file
    video_clip.write_videofile(output_file)
