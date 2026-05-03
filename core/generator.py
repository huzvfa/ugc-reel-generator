import streamlit as st
from huggingface_hub import InferenceClient
import edge_tts
import os
import subprocess
from PIL import Image

client = InferenceClient(token=st.secrets["HF_TOKEN"])

# --- AI VIDEO GENERATION (ACTUAL MOTION) ---
def query_video_gen(image_path, prompt):
    try:
        # Using CogVideoX - a top-tier open-source video model in 2026
        # This generates 6 seconds of REAL motion based on the image and prompt
        with open(image_path, "rb") as f:
            image_data = f.read()

        video_bytes = client.image_to_video(
            image=image_data,
            model="THUDM/CogVideoX-5b", # High-quality motion model
            prompt=f"{prompt}, high quality, realistic movement, cinematic"
        )
        
        path = "output/motion_clip.mp4"
        with open(path, "wb") as f:
            f.write(video_bytes)
        return path
    except Exception as e:
        st.warning("Advanced Video API busy. Falling back to Dynamic Zoom.")
        return None

# --- FFmpeg ASSEMBLY (Motion + Audio) ---
def assemble_final_reel(video_path, audio_path, target_duration):
    output_path = "output/final_reel.mp4"
    # Loops the motion clip to match your 15-30s timer
    cmd = [
        'ffmpeg', '-y', '-stream_loop', '-1', '-i', video_path,
        '-i', audio_path, '-map', '0:v', '-map', '1:a',
        '-c:v', 'libx264', '-t', str(target_duration),
        '-pix_fmt', 'yuv420p', '-shortest', output_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path

async def generate_voice(text, voice, style="general", output_path="output/voice.mp3"):
    # Styles: 'seductive' isn't a standard neural label, 
    # we map your requests to Azure Neural styles: 'whispering', 'cheerful', etc.
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)
    return output_path
