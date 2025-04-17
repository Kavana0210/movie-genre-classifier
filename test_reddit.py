import praw

reddit = praw.Reddit(
    client_id="client_id",  # Replace with your client ID
    client_secret="client_secret",  # Replace with your client secret
    user_agent="your_user_agent"  # Replace with your user agent
)

# Test fetching a submission
subreddit = reddit.subreddit("movies")
for submission in subreddit.hot(limit=1):
    print(submission.title)
