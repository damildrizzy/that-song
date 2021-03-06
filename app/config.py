import os
import logging
import json
from dotenv import load_dotenv
import tweepy
import cloudinary
import redis
from cloudinary import uploader, CloudinaryVideo


load_dotenv()
logger = logging.getLogger()

audd_api_token = os.getenv('AUDD_API_TOKEN')

since_id = os.getenv('SINCE_ID')

cloudinary.config(
  cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'),
  api_key = os.getenv('CLOUDINARY_API_KEY'),  
  api_secret = os.getenv('CLOUDINARY_API_SECRET')  
)

if os.getenv("CURRENT_ENV") == "development":
    redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)
else:
    redis_url = os.getenv("REDIS_URL")
    redis_db = redis.from_url(redis_url)
    # since_id = os.getenv("SINCE_ID")
    # redis_db.set("since_id", since_id)


def create_api():
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error Creating API", exc_info=True)
        raise e
    logger.info("API CREATED")
    return api
