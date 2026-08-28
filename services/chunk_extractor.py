import re
from youtube_transcript_api import YouTubeTranscriptApi

api = YouTubeTranscriptApi()

def extract_video_id(url: str) -> str:
    patterns = [
        r"(?:youtube\.com/watch\?v=)([^&]+)",
        r"(?:youtu\.be/)([^?&]+)",
        r"(?:youtube\.com/shorts/)([^?&]+)",
        r"(?:youtube\.com/embed/)([^?&]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError("Invalid YouTube URL: could not extract video ID")

def chunk_extractor(url: str) -> dict:
    try:
        video_id = extract_video_id(url)
        response = api.fetch(video_id, languages=["hi", "en"])
        response_text = " ".join(line.text for line in response)
        print(video_id)
        return {
            "text": response_text,
            "video_id": video_id
        }
    except Exception as e:
        print(f"error: {e}")
        raise Exception(f"Failed to extract transcript: {e}")

if __name__ == "__main__":
    result = chunk_extractor("https://www.youtube.com/watch?v=4JofSJIrjwU")
    print(result)