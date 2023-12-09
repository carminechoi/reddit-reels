"""Module to convert Text to Speech"""
from gtts import gTTS
from models.reddit_post import RedditPost
from config import AUDIO_FILE_PATH
import os


def text_to_speech(post: RedditPost) -> str:
    """
    Convert text to speech using Google's tts

    Parameters:
        text (str): Text to convert.

    Returns:
        file_path (str): Output audio file path.
    """
    # Delete file
    os.remove(AUDIO_FILE_PATH)

    character_count = 0

    def write_to_file(text):
        nonlocal character_count
        tts = gTTS(text, lang="en")
        with open(AUDIO_FILE_PATH, "ab") as f:
            tts.write_to_fp(f)
        character_count += len(text)

    for key, value in post.__dict__.items():
        if value:
            if key == "comments":
                for comment in value:
                    if character_count > 200:
                        break
                    write_to_file(comment.body)
            else:
                write_to_file(value)

    return AUDIO_FILE_PATH


if __name__ == "__main__":
    text_to_speech("testing audio")
