from tools import dataLoader

api_key = dataLoader.getConfigKey('api_key')
print(f'API key: {api_key}')

# main.py
import os
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tools.agent import createScript
from tools.datasaver import saveVideoScript
from tools.scriptToVideo import convert_to_mp4
from google.cloud import storage

# Configure where to stage scripts and videos inside the container:
TMP_DIR = "/tmp"
VIDEO_BUCKET = os.environ["VIDEO_BUCKET"]

app = FastAPI(title="Manim Video Generator API")

class GenerateRequest(BaseModel):
    prompt: str

class GenerateResponse(BaseModel):
    video_url: str

# Initialize GCS client once
gcs_client = storage.Client()

@app.post("/generate", response_model=GenerateResponse)
async def generate_video(req: GenerateRequest):
    try:
        # 1) Create Manim script
        script_text = createScript(req.prompt)
        script_name = f"{uuid.uuid4().hex}.py"
        script_path = os.path.join(TMP_DIR, script_name)
        saveVideoScript(script_text, script_path)

        # 2) Convert to mp4
        video_name = f"{uuid.uuid4().hex}.mp4"
        local_video_path = os.path.join(TMP_DIR, video_name)
        convert_to_mp4(script_path, local_video_path)

        # 3) Upload to GCS
        bucket = gcs_client.bucket(VIDEO_BUCKET)
        blob = bucket.blob(video_name)
        blob.upload_from_filename(local_video_path)

        # 4) Generate a time-limited signed URL
        url = blob.generate_signed_url(expiration=3600)

        return GenerateResponse(video_url=url)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
