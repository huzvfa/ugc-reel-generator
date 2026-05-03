import streamlit as st
from huggingface_hub import InferenceClient
import edge_tts
import os
import subprocess

client = InferenceClient(token=st.secrets["HF_TOKEN"])

def hover_generate_visual(prompt, mode, u1=None, u2=None):
    """Generates high-fidelity images for HOVER AI Vision Lab"""
    if not os.path.exists("output"): os.makedirs("output")
    path = os.path.abspath("output/hover_vision.png")
    
    if mode == "Image-to-Image" and u1:
        img = client.image_to_image(image=u1.getvalue(), prompt=prompt, model="lllyasviel/control_v11p_sd15_canny")
    else:
        img = client.text_to_image(f"{prompt}, high quality, realistic", model="black-forest-labs/FLUX.1-schnell")
    
    img.save(path)
    return path

def hover_generate_video(prompt, image_base_path, duration):
    """STRICT VIDEO GENERATION: Ensures .mp4 output only"""
    if not os.path.exists("output"): os.makedirs("output")
    motion_path = os.path.abspath("output/motion_raw.mp4")
    final_path = os.path.abspath("output/hover_final.mp4")
    
    try:
        # 1. GENERATE ACTUAL AI MOTION
        with open(image_base_path, "rb") as f:
            img_data = f.read()
        
        video_bytes = client.image_to_video(
            image=img_data,
            model="stabilityai/stable-video-diffusion-img2vid-xt"
        )
        with open(motion_path, "wb") as f:
            f.write(video_bytes)
            
        # 2. MASTER TO VERTICAL 9:16 (1080x1920)
        cmd = [
            'ffmpeg', '-y', '-stream_loop', '-1', '-i', motion_path,
            '-t', str(duration), '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
            '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
            final_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return final_path
    except Exception as e:
        st.error(f"Motion API Error: {e}")
        return None

async def hover_voice_engine(text, voice, path):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(path)
    return os.path.abspath(path)
