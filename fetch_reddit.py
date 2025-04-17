import praw
import pandas as pd
import re

# Preprocessing function
def preprocess_text(text):
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove special characters
    text = re.sub(r'\W', ' ', text)
    # Remove single characters
    text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# Replace with your credentials
reddit = praw.Reddit(
    client_id="client_id",  # Replace with your client ID
    client_secret="client_secret",  # Replace with your client secret
    user_agent="user_agent"  # Replace with your user agent
)

# Fetch comments from r/movies
subreddit = reddit.subreddit("movies")
comments = []
for comment in subreddit.comments(limit=100):  # Fetch 100 comments
    comments.append(comment.body)

# Save comments to a DataFrame
df = pd.DataFrame(comments, columns=["comment"])

# Apply preprocessing to the comments
df["cleaned_comment"] = df["comment"].apply(preprocess_text)
print(df.head())

# Save cleaned comments to a CSV file
df.to_csv("comments.csv", index=False)
