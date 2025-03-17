import praw

reddit = praw.Reddit(
    client_id="dLEFJwcRr6T2lMwiVGg2cw",  # Replace with your client ID
    client_secret="Qdcs7jRsujwBFSUMweTWf8ydqRb-Kw",  # Replace with your client secret
    user_agent="windows:MovieGenreClassifier:v1.0 (by /u/New-Joke-8982)"  # Replace with your user agent
)

# Test fetching a submission
subreddit = reddit.subreddit("movies")
for submission in subreddit.hot(limit=1):
    print(submission.title)