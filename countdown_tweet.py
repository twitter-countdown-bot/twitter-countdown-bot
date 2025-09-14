import os
from datetime import date
import tweepy

def days_left(release_iso: str) -> int:
    """Calculates the number of days until the release date."""
    release = date.fromisoformat(release_iso) # YYYY-MM-DD
    return (release - date.today()).days

def message(n: int) -> str:
    """Generates a tweet message based on the number of days left."""
    if n > 1:
        return f"#TheyCallHimOG releases in {n} days!\n#PawanKalyan"
    if n == 1:
        return "#TheyCallHimOG releases in 1 day!\n#PawanKalyan"
    if n == 0:
        # Applying the new format for release day as well
        return "#TheyCallHimOG releases today! 🎬🔥\n#PawanKalyan"
    # Applying the new format for after the release
    return "#TheyCallHimOG has released! Hope you enjoyed it!\n#PawanKalyan"

def main():
    try:
        # Get credentials from environment variables
        api_key = os.environ["API_KEY"]
        api_secret = os.environ["API_SECRET"]
        access_token = os.environ["ACCESS_TOKEN"]
        access_secret = os.environ["ACCESS_SECRET"]
        release_date = os.environ.get("RELEASE_DATE", "2025-09-27")
        
        # --- V2 AUTHENTICATION ---
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret
        )
        
        # Generate the tweet text using your existing functions
        text = message(days_left(release_date))
        
        # --- V2 TWEET POSTING ---
        print(f"Attempting to post tweet:\n---\n{text}\n---")
        response = client.create_tweet(text=text)
        
        print(f"🎉 Tweet posted successfully! Tweet ID: {response.data['id']}")

    except KeyError as e:
        print(f"❌ Error: Missing environment variable {e}. Please set all required credentials.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
