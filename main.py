"""Importing scripts"""
from scripts.reddit_api import fetch_reddit_post
from scripts.text_to_speech import text_to_speech
from config import SUBREDDIT


def main():
    """Main logic loop"""
    # Step 1: Fetch Reddit post
    reddit_post = fetch_reddit_post(SUBREDDIT)

    if reddit_post is None:
        print("No text based submission")
        return
    print(f"Retrieved {SUBREDDIT} post")

    # Step 2: Convert Reddit post content to speech
    audio_file_path = text_to_speech(reddit_post)
    print(f"Saved audio to {audio_file_path}")

    # Step 3: Capture gamplay footage

    # Step 4: Combine audio and gameplay video


if __name__ == "__main__":
    main()
