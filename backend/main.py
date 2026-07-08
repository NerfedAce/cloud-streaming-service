from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model import Form,Movie
from fastapi import HTTPException
from DBquery import get_data_by_id , get_data_by_user

app = FastAPI()
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_headers=["*"],allow_methods=["*"])


import subprocess
import json

def get_video_length(video_path: str) -> str:
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

    return f"{minutes}"


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
def login(form:Form):
    user = form.user
    password = form.password
    if user == "admin" and password == "":
        return {"status":200}
    raise HTTPException(status_code=400, detail="Incorrect username or password")
l = [Movie(title="Spider-Man: Homecoming" , length="133 minutes" ,id = 1 ,
           img="https://upload.wikimedia.org/wikipedia/en/f/f9/Spider-Man_Homecoming_poster.jpg",
           url = "https://www.w3schools.com/html/mov_bbb.mp4")]

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
def upload(form:Form):
    title = form.title
    video = form.video
    

