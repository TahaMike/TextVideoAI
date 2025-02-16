from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from text_to_video import generate_video_from_text

app = FastAPI()

class TextInput(BaseModel):
    text: str

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.post("/generate", response_class=FileResponse)
def generate_video(input_data: TextInput):
    try:
        video_path = generate_video_from_text(input_data.text)
        return FileResponse(video_path, media_type='video/mp4', filename='output.mp4')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
