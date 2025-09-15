import tweepy
import os
from datetime import date, timedelta

# Load API keys from environment variables
consumer_key = os.environ['TWITTER_API_KEY']
consumer_secret = os.environ['TWITTER_API_SECRET_KEY']
access_token = os.environ['TWITTER_ACCESS_TOKEN']
access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

# Authenticate with Tweepy
client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

# Calculate days until 27 September 2025
target_date = date(2025, 9, 27)
today = date.today()
days_remaining = (target_date - today - timedelta(days=1)).days

# Convert days_remaining to string and tweet it
tweet_text = f"{days_remaining} days left until 27 September 2025!"
response = client.create_tweet(text=tweet_text)

print("Tweet posted successfully:", response)
