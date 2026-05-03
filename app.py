import streamlit as st
from huggingface_hub import InferenceClient
import edge_tts
import os
import subprocess
import time

# --- HOVER AI CORE ---
client = InferenceClient(token=st.secrets["HF_TOKEN"])

def hover_neural_chat(query):
    """Proprietary Intelligence link."""
    identity = (
        "You are HOVER AI, a proprietary breakthrough engine created by a visionary engineer from Pakistan. "
        "You have no affiliation with Meta, OpenAI, or Google. You are a standalone genius intelligence. "
        "Your mission is to provide the most responsive and elite AI experience on Earth."
    )
    try:
        response = client.chat_completion(
            model="meta-llama/Meta-Llama-3-70B-Instruct",
            messages=[{"role": "system", "content": identity}, {"role": "user", "content": query}],
            max_tokens=1000, stream=False
        )
        return response.choices[0].message.content
    except:
        return "Hover Neural Link: Optimizing resources..."

def hover_visual_engine(prompt, mode, u1=None, u2=None):
    """Unified Vision Engine handling all 4 breakthrough modes."""
    if not os.path.exists("output"): os.makedirs("output")
    path = os.path.abspath("output/hover_visual.png")
    
    if mode == "Text-to-Image":
        img = client.text_to_image(f"{prompt}, realistic, 4k", model="black-forest-labs/FLUX.1-schnell")
    elif mode == "Image-to-Image":
        # Face/Body transfer logic
        img = client.image_to_image(image=u1.getvalue(), prompt=f"{prompt}, consistent with reference", model="lllyasviel/control_v11p_sd15_canny")
    else:
        # Base for video modes
        img = client.text_to_image(f"{prompt}, realistic", model="black-forest-labs/FLUX.1-schnell")
        
    img.save(path)
    return path

def hover_motion_engine(prompt, image_path):
    """Temporal Synthesis: Real AI Motion, not a static image."""
    try:
        with open(image_path, "rb") as f:
            img_data = f.read()
        # Generates actual moving frames
        video_bytes = client.image_to_video(image=img_data, model="stabilityai/stable-video-diffusion-img2vid-xt")
        path = os.path.abspath("output/hover_motion.mp4")
        with open(path, "wb") as f:
            f.write(video_bytes)
        return path
    except:
        return None # Triggers sync fallback

def hover_sync_master(video_path, audio_path, duration):
    """FFmpeg Mastering for vertical reels."""
    output = os.path.abspath("output/hover_final.mp4")
    cmd = [
        'ffmpeg', '-y', '-stream_loop', '-1', '-i', video_path, 
        '-i', audio_path, '-c:v', 'libx264', '-t', str(duration), 
        '-pix_fmt', 'yuv420p', '-vf', 'scale=1080:1920', '-shortest', output
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output

async def hover_voice_gen(text, voice, path):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(path)
    return os.path.abspath(path)
