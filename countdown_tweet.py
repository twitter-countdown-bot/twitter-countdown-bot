import os
from datetime import date, datetime
import tweepy

def days_left(release_iso: str) -> int:
    release = date.fromisoformat(release_iso) # YYYY-MM-DD
    return (release - date.today()).days

def message(n: int) -> str:
    # Get today's date to make the tweet unique every day
    today_str = date.today().strftime("%b %d") # Formats date like "Sep 15"

    if n > 1:
        return f"({today_str}) TheyCallHimOG releases in {n} days! #OG #TheyCallHimOG #PawanKalyan #Countdown"
    if n == 1:
        return f"({today_str}) TheyCallHimOG releases in 1 day! #OG #TheyCallHimOG #PawanKalyan #Countdown"
    if n == 0:
        return f"({today_str}) TheyCallHimOG releases today! 🎬🔥 #OG #TheyCallHimOG #PawanKalyan"
    
    return f"({today_str}) TheyCallHimOG has released! Hope you enjoyed it! #OG #TheyCallHimOG #PawanKalyan"

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
    
    # This print statement includes a timestamp to help debug date/time issues
    print(f"Script executed at {datetime.utcnow().isoformat()} UTC. Tweet: {text}")

if __name__ == "__main__":
    main()
