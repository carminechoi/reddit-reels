"""Importing scripts"""
from scripts.reddit_api import fetch_reddit_post
from scripts.text_to_speech import text_to_speech
from config import SUBREDDIT


def main():
    """Main logic loop"""
    # Step 1: Fetch Reddit post
    reddit_post = fetch_reddit_post(SUBREDDIT)

    if reddit_post is None:
        pass

    # Step 2: Convert Reddit post content to speech
    title = reddit_post.title
    file_path = text_to_speech(title)

    # Step 3: Capture gamplay footage

    # Step 4: Combine audio and gameplay video


if __name__ == "__main__":
    main()
