import streamlit as st
from huggingface_hub import InferenceClient
import edge_tts
import os

client = InferenceClient(token=st.secrets["HF_TOKEN"])

def query_image_gen(prompt):
    # Fastest 2026 Model: FLUX Schnell
    image = client.text_to_image(f"{prompt}, high quality, realistic ugc", model="black-forest-labs/FLUX.1-schnell")
    if not os.path.exists("output"): os.makedirs("output")
    path = "output/base.png"
    image.save(path)
    return path

def query_im2im_gen(u1, u2, prompt):
    if not os.path.exists("output"): os.makedirs("output")
    # Face reference logic
    img = client.image_to_image(image=u1.getvalue(), prompt=f"{prompt}, maintain reference features", model="lllyasviel/control_v11p_sd15_canny")
    path = "output/im2im.png"
    img.save(path)
    return path

def query_video_gen(image_path, prompt):
    try:
        with open(image_path, "rb") as f:
            image_data = f.read()
        # Direct Video Task
        video_bytes = client.image_to_video(image=image_data, model="stabilityai/stable-video-diffusion-img2vid-xt")
        path = "output/motion.mp4"
        with open(path, "wb") as f:
            f.write(video_bytes)
        return path
    except:
        return "fallback"

async def generate_voice(text, voice, path):
    if not os.path.exists("output"): os.makedirs("output")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(path)
    return path
