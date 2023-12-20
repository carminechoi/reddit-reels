"""Importing scripts"""
from scripts.reddit import fetch_reddit_post
from scripts.audio import text_to_speech
from scripts.video import create_video
from scripts.delete import (
    delete_screenshots,
    delete_audio_file,
    delete_video_file,
)
from game.flappy_bird_game import FlappyBirdGame
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
    game = FlappyBirdGame()
    game.run(100)
    print("Completed game")

    # Step 4: Combine audio and gameplay screenshots
    create_video()
    print("Saved video")

    # Step 5: Upload video

    # Step 6: Delete media files
    delete_screenshots()
    delete_audio_file()
    # delete_video_file()
    print("Deleted media files")


if __name__ == "__main__":
    main()
