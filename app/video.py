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
        video = VideoFileClip(url).subclip(0,20)
        #convert to mp3
        audio = video.audio
        #saves audio to local directory
        audio.write_audiofile(f"{tweet_id}.mp3")
        #upload to cloudinary
        upload_mp3 = uploader.upload(f"{tweet_id}.mp3", resource_type="video", public_id=f"{tweet_id}")
        url = upload_mp3['secure_url']
        data = {
            'url': url,
            'api_token': audd_api_token
        }
        result = requests.post('https://api.audd.io', data=data)
        return json.loads(result.text)
