"""Modules to interact with Reddit's API"""
import praw
from config import (
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_USER_AGENT,
)
from models.reddit_post import RedditPost
from models.reddit_comment import RedditComment


def fetch_reddit_post(subreddit_name: str) -> RedditPost:
    """
    Fetch the top post of the day from the specified subreddit

    Parameters:
        subreddit_name (str): The name of the subreddit.

    Returns:
        RedditPost: An instance of RedditPost representing the top, text-based post.
    """
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT,
    )

    subreddit = reddit.subreddit(subreddit_name)

    top_submission = subreddit.top(time_filter="day")

    for submission in top_submission:
        # Find text submission
        if submission.selftext:
            # Create comment list
            comments = create_comment_list(submission.comments)

            # Create reddit post object
            reddit_post = RedditPost(
                submission.title,
                submission.selftext,
                submission.author,
                comments,
            )
            return reddit_post


def create_comment_list(comments) -> list[RedditComment]:
    """
    Create a list of RedditComment objects from a comments object.

    Parameters:
        comments: The comments object.

    Returns:
        list[RedditComment]: List of RedditComment objects.
    """
    reddit_comments = []

    for comment in comments:
        reddit_comments.append(
            RedditComment(comment.author, comment.body, comment.score)
        )

    return reddit_comments


if __name__ == "__main__":
    post_content = fetch_reddit_post("askreddit")
    print(f"Fetched Reddit post content: {post_content}")
