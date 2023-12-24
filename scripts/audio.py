"""Module to convert Text to Speech"""
import os
from gtts import gTTS
import eyed3
from models.reddit_post import RedditPost
from config import AUDIO_FILE_PATH, CHARACTER_COUNT


def get_mp3_duration(file_path):
    """
    Get mp3 duration in seconds
    """
    audiofile = eyed3.load(file_path)
    if audiofile is not None:
        return audiofile.info.time_secs
    return None


def delete_file_if_exists(path):
    """
    Delete the file if it exists
    """
    if os.path.exists(path):
        os.remove(path)


def text_to_speech(post: RedditPost) -> str:
    """
    Convert text to speech using Google's tts

    Parameters:
        text (str): Text to convert.

    Returns:
        file_path (str): Output audio file path.
    """
    delete_file_if_exists(AUDIO_FILE_PATH)

    character_count = 0

    def write_to_file(text):
        nonlocal character_count
        tts = gTTS(
            text,
            lang="en",
            slow=False,
        )
        with open(AUDIO_FILE_PATH, "ab") as f:
            tts.write_to_fp(f)
        character_count += len(text)

    for key, value in post.__dict__.items():
        if value:
            if key == "comments":
                for comment in value:
                    if character_count > CHARACTER_COUNT:
                        break
                    write_to_file(comment.body)
            else:
                write_to_file(value)

    return AUDIO_FILE_PATH


if __name__ == "__main__":
    text_to_speech("testing audio")
