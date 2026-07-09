from fastapi import FastAPI,UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddlewarestr
from model import form,Movie
from fastapi import HTTPException
from DBquery import get_data_by_id , get_data_by_user , add_data
from dotenv import load_dotenv

app = FastAPI()
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_headers=["*"],allow_methods=["*"])
load_dotenv()

import subprocess
import json
import os
import uuid
import shutil
import tempfile
import boto3

AWS_REGION = os.getenv("AWS_REGION")
AWS_BUCKET = os.getenv("AWS_BUCKET")
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=AWS_REGION,
)

def upload_to_s3(file_path: str, key: str):
    s3.upload_file(file_path, AWS_BUCKET, key)

    return f"https://{AWS_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{key}"


def get_video_length(video_path: str) -> int:
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            video_path,
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    data = json.loads(result.stdout)

    duration = float(data["format"]["duration"])

    minutes = int(duration // 60)
    seconds = int(duration % 60)

    return minutes


def generate_thumbnail(video_path: str, thumbnail_path: str):
    probe = subprocess.run(
        [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            video_path,
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    duration = float(json.loads(probe.stdout)["format"]["duration"])

    # halfway through the video
    timestamp = duration / 2

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-ss", str(timestamp),
            "-i", video_path,
            "-vframes", "1",
            thumbnail_path,
        ],
        check=True,
    )


@app.post("/login")
def login(form:form):
    user = form.user
    password = form.password
    if user == "admin" and password == "":
        return {"status":200}
    raise HTTPException(status_code=400, detail="Incorrect username or password")


@app.get("/api/videos/{user}")
def get_videos(user: str):
    l = get_data_by_user(user)
    return l

@app.get("/api/video/{id}")
def get_movie(id: int):
    l = get_data_by_id(id)
    if not l:
        raise HTTPException(status_code=404, detail="Movie not found")
    return l


@app.post("/upload/{user}")
async def upload(
    user: str,
    title: str = Form(...),
    video: UploadFile = File(...)
):
    temp_dir = tempfile.mkdtemp()

    try:
        # Save uploaded video
        ext = os.path.splitext(video.filename)[1]

        video_filename = f"{uuid.uuid4()}{ext}"
        video_path = os.path.join(temp_dir, video_filename)

        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)

        # Video length
        length = get_video_length(video_path)

        # Generate thumbnail
        thumb_filename = f"{uuid.uuid4()}.jpg"
        thumb_path = os.path.join(temp_dir, thumb_filename)

        generate_thumbnail(video_path, thumb_path)

        # Upload video to S3
        video_key = f"videos/{video_filename}"
        video_url = upload_to_s3(video_path, video_key)

        # Upload thumbnail to S3
        thumb_key = f"thumbnails/{thumb_filename}"
        thumb_url = upload_to_s3(thumb_path, thumb_key)

        # Store metadata


        add_data(
            title,
            video_url,
            thumb_url,
            length,
            user,
        )

        return {
            "status": "success",
            "id": video_id,
            "title": title,
            "url": video_url,
            "img": thumb_url,
            "length": length,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

