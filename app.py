import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import praw
import pandas as pd
import re
from transformers import BertTokenizer, BertForSequenceClassification
import torch

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

# Function to classify genre
def classify_genre(text):
    if not text:  # Skip empty strings
        return "Unknown"
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_genre = torch.argmax(logits, dim=-1).item()
    return genres[predicted_genre]

# Load tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=5)  # Adjust num_labels for your genres
genres = ["Action", "Comedy", "Drama", "Horror", "Sci-Fi"]

# Streamlit app
st.title("Movie Genre Classifier")

# Input for user to enter a movie name
movie_name = st.text_input("Enter a movie name:")

if st.button("Classify Genre"):
    if movie_name:
        # Fetch comments from Reddit
        reddit = praw.Reddit(
            client_id="dLEFJwcRr6T2lMwiVGg2cw",  # Replace with your client ID
            client_secret="Qdcs7jRsujwBFSUMweTWf8ydqRb-Kw",  # Replace with your client secret
            user_agent="windows:MovieGenreClassifier:v1.0 (by /u/New-Joke-8982)"  # Replace with your user agent
        )

        subreddit = reddit.subreddit("all")  # Use "all" subreddit for more comments
        comments = []
        st.write("Fetching comments...")
        progress_bar = st.progress(0)
        for i, submission in enumerate(subreddit.hot(limit=100)):  # Fetch 100 hot posts
            submission.comments.replace_more(limit=0)  # Limit comment depth
            for comment in submission.comments.list():  # Fetch comments from each post
                if movie_name.lower() in comment.body.lower():  # Filter comments containing the exact movie name
                    comments.append(comment.body)
            progress_bar.progress((i + 1) / 100)  # Update progress bar

        # Save comments to a DataFrame
        df = pd.DataFrame(comments, columns=["comment"])

        # Apply preprocessing to the comments
        df["cleaned_comment"] = df["comment"].apply(preprocess_text)

        # Classify each comment
        st.write("Classifying genres...")
        df["predicted_genre"] = df["cleaned_comment"].apply(classify_genre)

        # Display results
        st.write("### Comments and Predicted Genres")
        st.write(df)

        # Display the most common genre
        if not df.empty:
            most_common_genre = df["predicted_genre"].mode()[0]
            st.success(f"Predicted Genre: {most_common_genre}")
        else:
            st.warning("No comments found for this movie.")
    else:
        st.warning("Please enter a movie name.")