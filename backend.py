from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from datetime import datetime

app = FastAPI()

# Allow requests from anywhere (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_video_id(url: str):
    parsed_url = urlparse(url)
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        if parsed_url.path == '/watch':
            query_params = parse_qs(parsed_url.query)
            return query_params.get('v', [None])[0]
        elif parsed_url.path.startswith('/embed/'):
            return parsed_url.path.split('/embed/')[1]
    elif parsed_url.hostname == 'youtu.be':
        return parsed_url.path.lstrip('/')
    return None

@app.get("/")
async def root():
    return {"message": "YouTube Transcript API is running."}

@app.get("/process")
async def process_video(video_url: str):
    video_id = extract_video_id(video_url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid or unsupported YouTube URL format.")
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([item['text'] for item in transcript])
        data = {
            "video_id": video_id,
            "video_url": video_url,
            "transcript": text,
            "timestamp": datetime.now().isoformat()
        }
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Transcript not available: {str(e)}")
