import streamlit as st
from huggingface_hub import InferenceClient
import edge_tts
import os
import subprocess
import time

# Brain of Hover AI: Using Groq for the most responsive chat experience
# To keep it free, we use the HuggingFace Inference Client for models like Llama-3, Flux, and CogVideo
client = InferenceClient(token=st.secrets["HF_TOKEN"])

def hover_chat(query):
    """The elite Chat feature of Hover AI."""
    response = client.text_generation(
        query,
        model="meta-llama/Meta-Llama-3-70B-Instruct",
        max_new_tokens=500,
        stream=False
    )
    return response

def query_video_motion(prompt, image_path=None):
    """Generates ACTUAL AI Video Motion (Blinking, Walking, Talking)."""
    try:
        # CogVideoX-5b is the leading open-source motion model in 2026
        # If image_path is provided, it does Image-to-Video; otherwise, Text-to-Video
        if image_path:
            with open(image_path, "rb") as f:
                img_data = f.read()
            video_bytes = client.image_to_video(
                img_data,
                model="THUDM/CogVideoX-5b",
                prompt=f"{prompt}, realistic movement, high quality"
            )
        else:
            video_bytes = client.text_to_video(
                prompt,
                model="THUDM/CogVideoX-5b"
            )
            
        path = os.path.abspath("output/motion_raw.mp4")
        with open(path, "wb") as f:
            f.write(video_bytes)
        return path
    except Exception as e:
        return None

def sync_audio_video(video_path, audio_path, duration):
    """Syncs the AI motion with the Voiceover script."""
    output_path = os.path.abspath("output/hover_final.mp4")
    # FFmpeg merges the actual AI motion with the AI voice
    cmd = [
        'ffmpeg', '-y', '-i', video_path, '-i', audio_path,
        '-c:v', 'libx264', '-t', str(duration), '-filter_complex',
        '[0:v]scale=1080:1920,setsar=1[v]', '-map', '[v]', '-map', '1:a',
        '-pix_fmt', 'yuv420p', '-shortest', output_path
    ]
    subprocess.run(cmd, check=True)
    return output_path
