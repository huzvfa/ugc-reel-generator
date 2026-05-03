import streamlit as st
from huggingface_hub import InferenceClient
import edge_tts
import os
import subprocess

client = InferenceClient(token=st.secrets["HF_TOKEN"])

def hover_generate_visual(prompt, mode, u1=None, u2=None):
    """Handles Text-to-Image and Image-to-Image (UGC style)"""
    if not os.path.exists("output"): os.makedirs("output")
    path = os.path.abspath("output/hover_vision.png")
    
    # Internal Prompt Expansion for breakthrough quality
    enhanced_prompt = f"{prompt}, ultra-realistic, 8k, cinematic, detailed ugc"

    if mode == "Image-to-Image" and u1:
        img = client.image_to_image(image=u1.getvalue(), prompt=enhanced_prompt, model="lllyasviel/control_v11p_sd15_canny")
    else:
        img = client.text_to_image(enhanced_prompt, model="black-forest-labs/FLUX.1-schnell")
    
    img.save(path)
    return path

def hover_generate_video(prompt, base_img, duration):
    """Temporal Synthesis: Real AI motion synced with FFmpeg"""
    final_v = os.path.abspath("output/hover_final.mp4")
    try:
        with open(base_img, "rb") as f:
            img_data = f.read()
        video_bytes = client.image_to_video(img_data, model="stabilityai/stable-video-diffusion-img2vid-xt")
        
        temp_v = os.path.abspath("output/temp_v.mp4")
        with open(temp_v, "wb") as f:
            f.write(video_bytes)
            
        cmd = [
            'ffmpeg', '-y', '-stream_loop', '-1', '-i', temp_v,
            '-t', str(duration), '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
            '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
            final_v
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return final_v
    except:
        return None

async def hover_voice_engine(text, voice, path):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(path)
    return os.path.abspath(path)
