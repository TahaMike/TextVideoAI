from diffusers import StableDiffusionPipeline
import torch
import numpy as np
import cv2
from datetime import datetime
import ffmpeg

# Load the text-to-image model
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float16).to("cuda")


def generate_video_from_text(text: str) -> str:
    fps = 2
    num_frames = 6  # Reduced for faster processing
    frame_width, frame_height = 512, 512
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    output_video = f"generated_video_{timestamp}.mp4"
    output_audio = f"generated_audio_{timestamp}.wav"
    output_final_video = f"final_video_{timestamp}.mp4"

    

    # Create video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video, fourcc, fps, (frame_width, frame_height))

    for frame_idx in range(num_frames):
        frame_prompt = f"{text}, frame {frame_idx}"
        image = pipe(frame_prompt).images[0]
        frame = np.array(image)
        video_writer.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    video_writer.release()

    # Merge audio and video using ffmpeg
    ffmpeg.input(output_video).input(output_audio).output(output_final_video, vcodec="libx264", acodec="aac").run(overwrite_output=True)

    return output_final_video
