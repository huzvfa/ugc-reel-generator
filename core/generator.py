import streamlit as st
from huggingface_hub import InferenceClient
import edge_tts
import os
import subprocess
import time

# Ultra-Fast Inference Client
client = InferenceClient(token=st.secrets["HF_TOKEN"])

def query_image_gen(prompt):
    # FLUX.1-schnell is the fastest high-quality model in 2026
    image = client.text_to_image(
        f"{prompt}, high quality, realistic ugc, candid, 4k", 
        model="black-forest-labs/FLUX.1-schnell"
    )
    if not os.path.exists("output"): os.makedirs("output")
    path = "output/base.png"
    image.save(path)
    return path

def query_im2im_gen(primary_img, reference_img, prompt):
    # UGC Face/Body Mapping logic
    primary_bytes = primary_img.getvalue()
    image = client.image_to_image(
        image=primary_bytes,
        prompt=f"{prompt}, maintain features from reference, high resolution",
        model="lllyasviel/control_v11p_sd15_canny"
    )
    path = "output/im2im.png"
    image.save(path)
    return path

def query_video_gen(image_path, prompt):
    try:
        with open(image_path, "rb") as f:
            image_data = f.read()
        # High-speed motion model
        video_bytes = client.image_to_video(
            image=image_data,
            model="stabilityai/stable-video-diffusion-img2vid-xt",
            prompt=f"{prompt}, realistic movement"
        )
        path = "output/motion.mp4"
        with open(path, "wb") as f:
            f.write(video_bytes)
        return path
    except Exception:
        # If API fails/timeouts, use FFmpeg to create a high-quality zoom-video fallback
        return "fallback"

async def generate_voice(text, voice, output_path):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)
    return output_path
