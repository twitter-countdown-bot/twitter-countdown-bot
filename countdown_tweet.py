import tweepy
import os
from datetime import datetime

# Authenticate to Twitter with environment variables (from GitHub secrets)
api_key = os.environ['API_KEY']
api_secret = os.environ['API_SECRET_KEY']
access_token = os.environ['ACCESS_TOKEN']
access_secret = os.environ['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
api = tweepy.API(auth)

# Event date
event_date = datetime(2025, 9, 25)
today = datetime.now()

days_left = (event_date - today).days

if days_left >= 0:
    message = (f"TheyCallHimOG releases in {days_left} days! Get ready to watch! "
               f"#OG #TheyCallHimOG #PawanKalyan #Countdown")
else:
    message = "TheyCallHimOG has released! Hope you enjoyed it! #OG #TheyCallHimOG #PawanKalyan"

api.update_status(message)
print("Tweet posted:", message)
