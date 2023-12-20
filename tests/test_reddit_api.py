"""Module to test functions related to Reddit's API"""
import unittest
from unittest.mock import patch
from scripts.reddit import (
    create_comment_list,
)
from models.reddit_comment import RedditComment


class TestRedditInteraction(unittest.TestCase):
    """
    Test suite for Reddit API interactions.
    """

    @patch("models.reddit_comment.RedditComment")
    def test_create_comment_list(self, mock_comment):
        """
        Test the create_comment_list function.

        Checks if the function correctly:
        1. creates a list of RedditComment objects from a given comments object
        2. creates an empty list from an empty comments list.
        """
        # Mocking a Reddit comment
        mock_comment.body = "Mock Body"
        mock_comment.score = 42

        # Mocking comments object
        mock_comments = [mock_comment]

        # Calling the function
        result = create_comment_list(mock_comments)

        # Asserting the result
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], RedditComment)
        self.assertEqual(result[0].body, "Mock Body")
        self.assertEqual(result[0].score, 42)

        # Mock an empty comment list
        result = create_comment_list([])

        # Asserting the result
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()
