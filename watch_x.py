import requests
import time
import os

USERNAME = "imassc_official"
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
CHECK_INTERVAL = 60

last_id = None

def get_latest_tweet():
    url = f"https://syndication.twitter.com/srv/timeline-profile/screen-name/{USERNAME}"
    r = requests.get(url)
    data = r.json()
    tweets = data["timeline"]["instructions"][0]["entries"]

    for entry in tweets:
        if "tweet" in entry["content"]["itemContent"]:
            tweet = entry["content"]["itemContent"]["tweet_results"]["result"]
            return tweet["rest_id"]
    return None

def send_to_discord(tweet_id):
    tweet_url = f"https://twitter.com/{USERNAME}/status/{tweet_id}"
    requests.post(WEBHOOK_URL, json={"content": tweet_url})

while True:
    try:
        tweet_id = get_latest_tweet()
        if tweet_id and tweet_id != last_id:
            send_to_discord(tweet_id)
            last_id = tweet_id
            print("Sent:", tweet_id)
    except Exception as e:
        print("Error:", e)

    time.sleep(CHECK_INTERVAL)
