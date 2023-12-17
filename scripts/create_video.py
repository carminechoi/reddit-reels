"""Module to generate video"""
import os
from moviepy.editor import ImageSequenceClip, AudioFileClip
from config import SCREENSHOT_FILE_PATH, AUDIO_FILE_PATH, VIDEO_FILE_PATH


def create_video():
    """Create video using audio and screenshots"""
    # File paths
    image_folder = SCREENSHOT_FILE_PATH
    audio_file = AUDIO_FILE_PATH
    output_file = VIDEO_FILE_PATH

    # Set audio for the video
    audio_clip = AudioFileClip(audio_file)

    # Create video clip from image sequence
    sequence_clip = ImageSequenceClip(
        [image_folder + img for img in os.listdir(image_folder)], fps=30
    )
    video_clip = sequence_clip.set_audio(audio_clip)
    video_clip.duration = audio_clip.duration
    video_clip.fps = 60

    # Write the video file
    video_clip.write_videofile(output_file)
