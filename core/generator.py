import streamlit as st
from huggingface_hub import InferenceClient
import edge_tts
import io
from PIL import Image

# Initialize Client
client = InferenceClient(token=st.secrets["HF_TOKEN"])

# --- 1. Text to Image ---
def query_image_gen(prompt):
    model_id = "black-forest-labs/FLUX.1-schnell"
    ugc_prompt = f"{prompt}, realistic UGC style, amateur smartphone photo, candid"
    
    image = client.text_to_image(ugc_prompt, model=model_id)
    path = "output_t2i.png"
    image.save(path)
    return path

# --- 2. Image to Image ---
def query_im2im_gen(uploaded_file, prompt):
    image_bytes = uploaded_file.getvalue()
    # Using a model that supports Image-to-Image tasks
    image = client.image_to_image(
        image=image_bytes,
        prompt=f"{prompt}, high quality, realistic",
        model="lllyasviel/control_v11p_sd15_canny" 
    )
    path = "output_i2i.png"
    image.save(path)
    return path

# --- 3. Image to Video ---
def query_video_gen(image_path, duration):
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        
        # Note: SVD generates short clips. 
        # For a 30s result, you would loop this clip in app.py using MoviePy
        video_bytes = client.post(
            data=image_bytes,
            model="stabilityai/stable-video-diffusion-img2vid-xt"
        )
        video_path = "output_clip.mp4"
        with open(video_path, "wb") as f:
            f.write(video_bytes)
        return video_path
    except Exception as e:
        st.error(f"Video Gen Error: {e}")
        return None

# --- 4. Voiceover Agent ---
async def generate_voice(text, voice, output_path="voice.mp3"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)
    return output_path
