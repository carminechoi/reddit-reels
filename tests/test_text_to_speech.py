"""Module to test functions related to Text to Speech"""
import unittest
from unittest.mock import patch, mock_open
from models.reddit_post import RedditPost
from config import AUDIO_FILE_PATH
from scripts.text_to_speech import delete_file_if_exists, text_to_speech


class TestTextToSpeech(unittest.TestCase):
    """
    Test suite for Text to Speech interactions.
    """

    @patch("os.path.exists", return_value=True)
    @patch("os.remove")
    def test_delete_existing_file(self, mock_exists, mock_remove):
        """
        Test deleting an existing file.
        """
        # Call the function
        delete_file_if_exists("test_file.txt")

        # Assert that os.path.exists was called with the correct path
        mock_exists.assert_called_once_with("test_file.txt")

        # Assert that os.remove was called with the correct path
        mock_remove.assert_called_once_with("test_file.txt")

    @patch("os.path.exists", return_value=False)
    @patch("os.remove")
    def test_delete_nonexistent_file(self, mock_remove, mock_exists):
        """
        Test deleting a nonexistent file.
        """
        # Call the function
        delete_file_if_exists("nonexistent_file.txt")

        # Assert that os.path.exists was called with the correct path
        mock_exists.assert_called_once_with("nonexistent_file.txt")

        # Assert that os.remove was not called since the file does not exist
        mock_remove.assert_not_called()

    def test_text_to_speech(self):
        """
        Test the text_to_speech function.
        """
        # Create a RedditPost object with some dummy data
        post = RedditPost(title="Test Title", selftext="Test Body", comments=[])

        # Calling the function
        result = text_to_speech(post)

        # Assert the result
        self.assertEqual(result, AUDIO_FILE_PATH)


if __name__ == "__main__":
    unittest.main()
