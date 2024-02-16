# reddit-reels

Transforming Reddit threads into short form videos

## Dependencies

Before getting started, ensure the following dependencies are installed:

-   [Python (version 3.9.13 or higher)](https://www.python.org/downloads/)
-   [pip (version 23.3.1 or higher)](https://pip.pypa.io/en/stable/installation/)

## Getting Started

1. **Clone the repository to your local machine:**

    ```
    git clone https://github.com/carminechoi/reddit-reels.git
    cd reddit-reels
    ```

2. Create and start virtual environment

    ```
    python -m venv venv
    venv\scripts\activate
    ```

3. Install the required dependencies.

    ```
    pip install -r requirements.txt
    ```

4. Create an environmental variables file named `.env` with your Reddit API credentials:

    ```
    REDDIT_CLIENT_ID=YOUR_REDDIT_CLIENT_ID
    REDDIT_CLIENT_SECRET=YOUR_REDDIT_CLIENT_SECRET
    REDDIT_USER_AGENT=YOUR_REDDIT_USER_AGENT
    ```

5. Run the application with
    ```
    python main.py
    ```

## Running Tests

To run the tests, use the following command:

```
python -m unittest discover tests
```

## License

This project is licensed under the MIT License
