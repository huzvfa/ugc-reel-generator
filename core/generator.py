import streamlit as st
from huggingface_hub import InferenceClient
import edge_tts
import os
import subprocess

client = InferenceClient(token=st.secrets["HF_TOKEN"])

def hover_generate_video(prompt, base_img, duration):
    """Deep synthesis for true AI motion reels."""
    if not os.path.exists("output"): os.makedirs("output")
    final_path = os.path.abspath("output/hover_final.mp4")
    
    try:
        with open(base_img, "rb") as f:
            img_data = f.read()
        # High-motion synthesis
        video_bytes = client.image_to_video(img_data, model="stabilityai/stable-video-diffusion-img2vid-xt")
        
        temp_v = os.path.abspath("output/temp_v.mp4")
        with open(temp_v, "wb") as f:
            f.write(video_bytes)
            
        cmd = [
            'ffmpeg', '-y', '-stream_loop', '-1', '-i', temp_v,
            '-t', str(duration), '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
            '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
            final_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return final_path
    except:
        return None
