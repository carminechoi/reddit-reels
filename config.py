"""Module to import environmental variables"""
from decouple import config

# Reddit API Configuration
REDDIT_CLIENT_ID = config("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = config("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = config("REDDIT_USER_AGENT")

SUBREDDIT = "showerthoughts"

# Text to Speech Configuration
AUDIO_FILE_PATH = "media/speech_audio.mp3"
CHARACTER_COUNT = 200


# Video Configuration
SCREENSHOT_FILE_PATH = "media/screenshots/"
VIDEO_FILE_PATH = "media/output.mp4"
