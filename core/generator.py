import streamlit as st
from huggingface_hub import InferenceClient
import edge_tts
import requests
import os
from PIL import Image

# Initialize Client for standard tasks
client = InferenceClient(token=st.secrets["HF_TOKEN"])

# --- 1. Text to Image (Flux Schnell) ---
def query_image_gen(prompt):
    ugc_prompt = f"{prompt}, realistic UGC style, amateur smartphone photo, candid"
    image = client.text_to_image(ugc_prompt, model="black-forest-labs/FLUX.1-schnell")
    if not os.path.exists("output"): os.makedirs("output")
    path = "output/t2i.png"
    image.save(path)
    return path

# --- 2. Image to Image (ControlNet) ---
def query_im2im_gen(uploaded_file, prompt):
    image_bytes = uploaded_file.getvalue()
    image = client.image_to_image(
        image=image_bytes,
        prompt=f"{prompt}, high quality, realistic",
        model="lllyasviel/control_v11p_sd15_canny" 
    )
    if not os.path.exists("output"): os.makedirs("output")
    path = "output/i2i.png"
    image.save(path)
    return path

# --- 3. Image to Video (The Robust Requests Fix) ---
def query_video_gen(image_path):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-video-diffusion-img2vid-xt"
    headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}

    try:
        with open(image_path, "rb") as f:
            data = f.read()
        
        # We use raw requests to avoid InferenceClient version mismatches
        response = requests.post(API_URL, headers=headers, data=data)
        
        if response.status_code == 200:
            if not os.path.exists("output"): os.makedirs("output")
            video_path = "output/clip.mp4"
            with open(video_path, "wb") as f:
                f.write(response.content)
            return video_path
        else:
            st.error(f"Video API Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        st.error(f"Video Generation Failed: {e}")
        return None

# --- 4. Voiceover Agent ---
async def generate_voice(text, voice, output_path="output/voice.mp3"):
    if not os.path.exists("output"): os.makedirs("output")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)
    return output_path
