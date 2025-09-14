import os
from datetime import date
import tweepy

def days_left(release_iso: str) -> int:
    release = date.fromisoformat(release_iso) # YYYY-MM-DD
    return (release - date.today()).days

def message(n: int) -> str:
    if n > 1:
        return f"TheyCallHimOG releases in {n} days! #OG #TheyCallHimOG #PawanKalyan #Countdown"
    if n == 1:
        return "TheyCallHimOG releases in 1 day! #OG #TheyCallHimOG #PawanKalyan #Countdown"
    if n == 0:
        return "TheyCallHimOG releases today! 🎬🔥 #OG #TheyCallHimOG #PawanKalyan"
    return "TheyCallHimOG has released! Hope you enjoyed it! #OG #TheyCallHimOG #PawanKalyan"

def main():
    api_key = os.environ["API_KEY"]
    api_secret = os.environ["API_SECRET"]
    access_token = os.environ["ACCESS_TOKEN"]
    access_secret = os.environ["ACCESS_SECRET"]
    release_date = os.environ.get("RELEASE_DATE", "2025-09-25")
    
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
    api = tweepy.API(auth)
    
    text = message(days_left(release_date))
    api.update_status(status=text)
    print("Tweet posted:", text)

if __name__ == "__main__":
    main()
