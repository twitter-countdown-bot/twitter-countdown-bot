import os
import time
from datetime import date
import tweepy

# --- Your list of movies to track ---
MOVIES = [
    {
        "title": "TheyCallHimOG",
        "main_hashtag": "#TheyCallHimOG",
        "secondary_hashtag": "#PawanKalyan",
        "release_date": "2025-09-27"
    },
    {
        "title": "Kantara: Chapter 1",
        "main_hashtag": "#KantaraChapter1",
        "secondary_hashtag": "#RishabShetty",
        "release_date": "2025-10-02"
    },
    # --- Your new movie ---
    {
        "title": "Baahubali The Epic",
        "main_hashtag": "#BaahubaliTheEpic",
        "secondary_hashtag": "#Prabhas #SSRajamouli",
        "release_date": "2027-12-17"  # NOTE: This is a placeholder date!
    },
]

def days_left(release_iso: str) -> int:
    """Calculates the number of days until the release date."""
    release = date.fromisoformat(release_iso)
    return (release - date.today()).days

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
        # Get credentials from environment variables
        api_key = os.environ["API_KEY"]
        api_secret = os.environ["API_SECRET"]
        access_token = os.environ["ACCESS_TOKEN"]
        access_secret = os.environ["ACCESS_SECRET"]
        
        # Authenticate with the v2 Client
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret
        )
        
        print("Starting daily movie countdown tweets...")
        
        # Loop through each movie in the list
        for movie in MOVIES:
            title = movie["title"]
            release_date = movie["release_date"]
            print(f"\nProcessing: {title}")

            days = days_left(release_date)

            if days < -7:
                print(f"'{title}' was released more than a week ago. Skipping.")
                continue

            # Generate the specific message for this movie
            text = generate_message(days, movie)
            
            # Post the tweet
            try:
                print(f"Attempting to post tweet:\n---\n{text}\n---")
                response = client.create_tweet(text=text)
                print(f"🎉 Tweet posted successfully for {title}! Tweet ID: {response.data['id']}")
            except Exception as e:
                print(f"❌ Error posting tweet for {title}: {e}")

            # Wait for a few seconds between tweets
            if movie != MOVIES[-1]:
                 print("Waiting for 15 seconds before the next tweet...")
                 time.sleep(15)

        print("\n✅ All movie tweets processed for today.")

    except KeyError as e:
        print(f"❌ Error: Missing environment variable {e}. Please set all required credentials.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
