import logging
import tweepy
import time
import pprint
import json
import random

from config import create_api, redis_db
from video import process_video
from utils import  success_responses, failure_responses

pp = pprint.PrettyPrinter(indent=4)

logging.basicConfig(filename='app.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, since_id):
    logger.info("Checking for new mentions")
    new_since_id = since_id
    tweets = tweepy.Cursor(api.mentions_timeline, since_id=since_id).items()
    for tweet in tweets:
        print("found a tweet")
        print(tweet.id)
        new_since_id = max(tweet.id, new_since_id)
        #save the since_id to redis so we can resume from here if we restart the server
        redis_db.set('since_id', new_since_id)
        if tweet.in_reply_to_status_id is None:
            continue
        replied_tweet_id = tweet.in_reply_to_status_id
        
        #check if that tweet already exists
        if redis_db.get(f"{replied_tweet_id}") is not None:
            print("found that one before")
            process = json.loads(redis_db.get(f"{replied_tweet_id}"))
        else:
            replied_tweet = api.get_status(replied_tweet_id)
            try:
                video_url = replied_tweet.extended_entities['media'][0]['video_info']['variants'][2]['url']
            except AttributeError:
                continue
            video_duration = replied_tweet.extended_entities['media'][0]['video_info']['duration_millis'] 
            #convert milliseconds to seconds
            video_duration = video_duration * 0.001
            process = process_video(video_url, video_duration, replied_tweet_id)
            print(process)
            print(type(process))
            #save the result to redis 
            tweet_data = json.dumps(process)
            redis_db.set(f"{replied_tweet_id}", tweet_data)
        
        if process['result'] is not None:

            title = process['result']['title']
            artist = process['result']['artist']
            song_link = process['result']['song_link']
            

            
            #reply the tweet
            prefix = random.choice(success_responses)
            api.update_status(
                status=f"@{tweet.user.screen_name} {prefix} The song is {title} by {artist}. You can get it here {song_link}",
                in_reply_to_status_id=tweet.id
            )
        else:
            prefix = random.choice(failure_responses)
            api.update_status(
                status=f"@{tweet.user.screen_name} {prefix}",
                in_reply_to_status_id=tweet.id
            )

    return new_since_id



def main():
    api = create_api()
    since_id =  int(redis_db.get('since_id'))
    while True:
        since_id = check_mentions(api, since_id)
        time.sleep(60)
    

if __name__ == "__main__":
    main()