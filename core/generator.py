import streamlit as st
from huggingface_hub import InferenceClient
import edge_tts
import io
import os
from PIL import Image

# Initialize Client
client = InferenceClient(token=st.secrets["HF_TOKEN"])

def query_image_gen(prompt):
    model_id = "black-forest-labs/FLUX.1-schnell"
    ugc_prompt = f"{prompt}, realistic UGC style, amateur smartphone photo, candid"
    image = client.text_to_image(ugc_prompt, model=model_id)
    if not os.path.exists("output"): os.makedirs("output")
    path = "output/t2i.png"
    image.save(path)
    return path

def query_im2im_gen(uploaded_file, prompt):
    image_bytes = uploaded_file.getvalue()
    # Task-specific call for Image-to-Image
    image = client.image_to_image(
        image=image_bytes,
        prompt=f"{prompt}, high quality, realistic",
        model="lllyasviel/control_v11p_sd15_canny" 
    )
    if not os.path.exists("output"): os.makedirs("output")
    path = "output/i2i.png"
    image.save(path)
    return path

def query_video_gen(image_path):
    try:
        with open(image_path, "rb") as f:
            image_data = f.read()
            
        # 🚀 FIX: Using the low-level request method for Video Tasks
        # This replaces .post() and .request_papi()
        response = client.request(
            method="POST",
            path="stabilityai/stable-video-diffusion-img2vid-xt",
            data=image_data
        )
        
        if not os.path.exists("output"): os.makedirs("output")
        video_path = "output/clip.mp4"
        with open(video_path, "wb") as f:
            f.write(response) # 'response' contains the binary video data
        return video_path
    except Exception as e:
        st.error(f"Video Gen Error: {e}")
        return None

async def generate_voice(text, voice, output_path="output/voice.mp3"):
    if not os.path.exists("output"): os.makedirs("output")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)
    return output_path
