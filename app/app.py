import logging
import tweepy
import time
import pprint

from config import create_api
from video import process_video

pp = pprint.PrettyPrinter(indent=4)

logging.basicConfig(filename='app.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, since_id):
    logger.info("Checking for new mentions")
    new_since_id = since_id
    tweets = tweepy.Cursor(api.mentions_timeline, since_id=since_id).items()
    for tweet in tweets:
        new_since_id = max(tweet.id, new_since_id)
        replied_tweet_id = tweet.in_reply_to_status_id
        replied_tweet = api.get_status(replied_tweet_id)
        video_url = replied_tweet.extended_entities['media'][0]['video_info']['variants'][2]['url']
        video_duration = replied_tweet.extended_entities['media'][0]['video_info']['duration_millis'] 
        video_duration = video_duration * 0.001
        process = process_video(video_url, video_duration, replied_tweet_id)
        title = process['result']['title']
        artist = process['result']['artist']
        api.update_status(
            status=f"The song name is {title} by {artist}",
            in_reply_to_status_id=tweet.id
        )

    return new_since_id



def main():
    api = create_api()
    since_id = 1
    while True:
        since_id = check_mentions(api, since_id)
        time.sleep(60)
    

if __name__ == "__main__":
    main()