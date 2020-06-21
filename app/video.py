import requests
import json
from config import audd_api_token, uploader, utils
from moviepy.editor import VideoFileClip




def process_video(url, duration, tweet_id):
    
    #The api doesnt's allow media longer than 20 seconds
    if duration <= 20:
        data = {
            'url': url,
            'api_token': audd_api_token
        }
        result = requests.post('https://api.audd.io/', data=data)
        return json.loads(result.text)
    else:
        #Trim video to 20 seconds
        # video = VideoFileClip(url).subclip(0,20)
        # #convert to mp3
        # audio = video.audio
        # #saves audio to local directory
        # audio.write_audiofile(f"{tweet_id}.mp3")
        #upload to cloudinary
        uploader.upload(url, resource_type="video", public_id=f"{tweet_id}")
        url = f"http://res.cloudinary.com/parselfinger/video/upload/eo_19.50,so_0.00/{tweet_id}.mp4"
        data = {
            'url': url,
            'api_token': audd_api_token
        }
        result = requests.post('https://api.audd.io', data=data)
        uploader.destroy(f"{tweet_id}", resource_type="video")
        return json.loads(result.text)
