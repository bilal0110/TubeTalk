import os
import re
from youtube_transcript_api import YouTubeTranscriptApi
api = YouTubeTranscriptApi()

def chunk_extractor(url:str)-> dict:

    try:
        #youtube video url id
        video_id =str(url.split("v=")[1][:12])
        response = api.fetch(video_id, languages=["hi","en"])

        response_text = " ".join(line.text for line in response)
        print(video_id)
        return {
            "text": response_text,
            "video_id": video_id
        }
    
    
    except Exception as e:
        print(f"error: {e}")
        raise Exception(f"Failed to to extract transcript")

if __name__ == "__main__":

        result=  chunk_extractor("https://www.youtube.com/watch?v=4JofSJIrjwU")
        print(result)


