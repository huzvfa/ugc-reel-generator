import streamlit as st
from huggingface_hub import InferenceClient
import edge_tts
import asyncio
from PIL import Image

client = InferenceClient(token=st.secrets["HF_TOKEN"])

# --- Voiceover Logic ---
async def generate_voice(text, voice, output_path="output/voice.mp3"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)
    return output_path

# --- Video Generation Logic ---
def query_video_gen(image_path, duration):
    # Stable Video Diffusion is the standard for Image-to-Video
    # Free API usually limits to short clips (~2-5s), we loop them for 30s
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        
        # Calling the SVD model
        video_bytes = client.post(
            data=image_bytes,
            model="stabilityai/stable-video-diffusion-img2vid-xt"
        )
        video_path = "output/clip.mp4"
        with open(video_path, "wb") as f:
            f.write(video_bytes)
        return video_path
    except Exception as e:
        st.error(f"Video Gen Error: {e}")
        return None
