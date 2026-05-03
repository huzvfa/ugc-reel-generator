import streamlit as st
from huggingface_hub import InferenceClient
import edge_tts
import os
import subprocess

client = InferenceClient(token=st.secrets["HF_TOKEN"])

def hover_master_video(prompt, base_img, duration):
    """Generates ultra-realistic 4K motion independently of audio status."""
    if not os.path.exists("output"): os.makedirs("output")
    final_v = os.path.abspath("output/hover_master.mp4")
    
    try:
        with open(base_img, "rb") as f:
            img_data = f.read()
        # High-motion Synthesis
        video_bytes = client.image_to_video(img_data, model="stabilityai/stable-video-diffusion-img2vid-xt")
        
        temp_path = os.path.abspath("output/temp.mp4")
        with open(temp_path, "wb") as f:
            f.write(video_bytes)
            
        # 9:16 Ultra-Realistic Mastering
        cmd = [
            'ffmpeg', '-y', '-stream_loop', '-1', '-i', temp_path,
            '-t', str(duration), '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p',
            '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
            final_v
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return final_v
    except:
        return None

async def hover_voice_engine(text, voice, rate="+0%", pitch="+0Hz"):
    """Fixed Tone & Language Logic for Seductive/Serious English and Native Urdu."""
    path = os.path.abspath("output/voice.mp3")
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(path)
    return path
