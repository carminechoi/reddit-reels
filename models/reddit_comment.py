class RedditComment:
    """Represents a Reddit comment"""

    def __init__(
        self,
        author,
        body,
        score,
    ):
        self.author = author
        self.body = body
        self.score = score
