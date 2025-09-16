import os
import time
from datetime import datetime
import tweepy
import pytz
import requests
import io

# --- Add your movie list with image URLs here ---
MOVIES = [
    {
        "title": "TheyCallHimOG",
        "main_hashtag": "#TheyCallHimOG",
        "secondary_hashtag": "#PawanKalyan",
        "release_date": "2025-09-25",
        "image_url": "https://pbs.twimg.com/media/G05bgvQakAAyh6m?format=jpg&name=large" # <-- Example URL
    },
    {
        "title": "Kantara: Chapter 1",
        "main_hashtag": "#KantaraChapter1",
        "secondary_hashtag": "#RishabShetty",
        "release_date": "2025-10-02",
        "image_url": "https://pbs.twimg.com/media/G0yd4TZawAAKiUx?format=jpg&name=medium" # <-- Example URL
    },
    {
        "title": "Baahubali The Epic",
        "main_hashtag": "#BaahubaliTheEpic",
        "secondary_hashtag": "#Prabhas #SSRajamouli",
        "release_date": "2025-10-31",
        "image_url": "https://pbs.twimg.com/media/Gzv5bwDbYAA8FXr?format=jpg&name=large" # <-- Example URL
    },
    {
        "title": "PEDDI",
        "main_hashtag": "#PEDDI",
        "secondary_hashtag": "#RamCharan #BuchiBabu",
        "release_date": "2026-03-27",
        "image_url": "https://pbs.twimg.com/media/GnBJpAIaYAE1J4_?format=jpg&name=large" # <-- Example URL
    },
]

def days_left(release_iso: str) -> int:
    """Calculates the number of days until the release date in IST."""
    ist_zone = pytz.timezone("Asia/Kolkata")
    today_ist = datetime.now(ist_zone).date()
    release = datetime.fromisoformat(release_iso).date()
    return (release - today_ist).days

def generate_message(n: int, movie: dict) -> str:
    """Generates a generic tweet message for any movie."""
    main_hashtag = movie["main_hashtag"]
    secondary_hashtag = movie["secondary_hashtag"]
    
    if n > 1:
        return f"{main_hashtag} releases in {n} days!\n{secondary_hashtag}"
    if n == 1:
        return f"{main_hashtag} releases in 1 day!\n{secondary_hashtag}"
    if n == 0:
        return f"{main_hashtag} releases today! 🔥\n{secondary_hashtag}"
    
    return f"{main_hashtag} has been released! Hope you enjoyed it!\n{secondary_hashtag}"

def main():
    try:
        # --- Authentication ---
        api_key = os.environ["API_KEY"]
        api_secret = os.environ["API_SECRET"]
        access_token = os.environ["ACCESS_TOKEN"]
        access_secret = os.environ["ACCESS_SECRET"]
        
        # We need both the v2 Client (for tweeting) and v1.1 API (for media uploads)
        client = tweepy.Client(
            consumer_key=api_key, consumer_secret=api_secret,
            access_token=access_token, access_token_secret=access_secret
        )
        auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
        api = tweepy.API(auth)
        
        print("Starting daily movie countdown tweets...")
        
        for movie in MOVIES:
            title = movie["title"]
            print(f"\nProcessing: {title}")

            days = days_left(movie["release_date"])

            if days < -7:
                print(f"'{title}' was released more than a week ago. Skipping.")
                continue

            # --- Media Upload Logic ---
            media_ids = []
            if movie.get("image_url"):
                try:
                    # Download the image from the URL
                    response = requests.get(movie["image_url"])
                    response.raise_for_status()
                    
                    # Upload the image from memory to Twitter
                    image_file = io.BytesIO(response.content)
                    media = api.media_upload(filename=f"{title}.jpg", file=image_file)
                    media_ids.append(media.media_id)
                    print(f"Image for {title} uploaded successfully.")
                except Exception as e:
                    print(f"❌ Could not upload image for {title}: {e}")

            # --- Generate message and Post Tweet ---
            text = generate_message(days, movie)
            
            try:
                print(f"Attempting to post tweet:\n---\n{text}\n---")
                # Attach the media_ids list to the tweet
                response = client.create_tweet(text=text, media_ids=media_ids)
                print(f"🎉 Tweet posted successfully for {title}! Tweet ID: {response.data['id']}")
            except Exception as e:
                print(f"❌ Error posting tweet for {title}: {e}")

            # Wait between tweets to avoid rate limits
            if movie != MOVIES[-1]:
                print("Waiting for 15 seconds before the next tweet...")
                time.sleep(15)

        print("\n✅ All movie tweets processed for today.")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
