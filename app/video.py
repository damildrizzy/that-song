import requests
import json
from config import audd_api_token, uploader


def process_video(url, duration, tweet_id):
    
    #The api doesnt's allow media longer than 20 seconds
    if duration <= 20:
        #run it by the music recog api
        data = {
            'url': url,
            'api_token': audd_api_token
        }
        result = requests.post('https://api.audd.io/', data=data)
        return json.loads(result.text)
    else:
        #upload to cloudinary
        uploader.upload(url, resource_type="video", public_id=f"{tweet_id}")
        
        #trim to first 20 secs
        url = f"http://res.cloudinary.com/parselfinger/video/upload/eo_19.50,so_0.00/{tweet_id}.mp4"
        
        #run it by the music recog api
        data = {
            'url': url,
            'api_token': audd_api_token
        }
        result = requests.post('https://api.audd.io', data=data)
        
        # delete the video before cloudinary bills the fuck out of me
        uploader.destroy(f"{tweet_id}", resource_type="video")
        return json.loads(result.text)
