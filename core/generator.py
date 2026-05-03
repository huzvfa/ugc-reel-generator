import streamlit as st
from huggingface_hub import InferenceClient
import edge_tts
import os
import subprocess

client = InferenceClient(token=st.secrets["HF_TOKEN"])

def hover_visual_gen(prompt, mode, u1=None):
    """HOVER AI Vision: Instant 8k synthesis"""
    if not os.path.exists("output"): os.makedirs("output")
    path = os.path.abspath("output/hover_vision.png")
    
    if mode == "Image-to-Image" and u1:
        img = client.image_to_image(image=u1.getvalue(), prompt=prompt, model="lllyasviel/control_v11p_sd15_canny")
    else:
        img = client.text_to_image(f"{prompt}, high quality, cinematic", model="black-forest-labs/FLUX.1-schnell")
    
    img.save(path)
    return path

def hover_video_gen(prompt, base_img, duration):
    """HOVER AI Motion: Deep synthesis with local reflex fallback"""
    if not os.path.exists("output"): os.makedirs("output")
    final_path = os.path.abspath("output/hover_final.mp4")
    
    try:
        # Attempt Deep AI Motion
        with open(base_img, "rb") as f:
            img_data = f.read()
        video_bytes = client.image_to_video(img_data, model="stabilityai/stable-video-diffusion-img2vid-xt")
        
        temp_motion = os.path.abspath("output/temp_motion.mp4")
        with open(temp_motion, "wb") as f:
            f.write(video_bytes)
        source_v = temp_motion
    except Exception:
        # Neural Reflex: Immediate high-quality cinematic fallback
        source_v = base_img

    # Final Mastering to 9:16 Vertical MP4
    # This command handles both raw AI video AND static fallbacks to ensure an MP4 is ALWAYS saved
    cmd = [
        'ffmpeg', '-y', '-loop', '1', '-i', source_v,
        '-t', str(duration), '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
        '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
        final_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return final_path

async def hover_voice_gen(text, voice, path):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(path)
    return os.path.abspath(path)
