"""Importing scripts"""
from scripts import reddit_api
from config import SUBREDDIT


def main():
    """Main logic loop"""
    # Step 1: Fetch Reddit post
    reddit_post = reddit_api.fetch_reddit_post(SUBREDDIT)

    if reddit_post is None:
        pass

    # Step 2: Convert Reddit post content to speech

    # Step 3: Capture gamplay footage

    # Step 4: Combine audio and gameplay video


if __name__ == "__main__":
    main()
