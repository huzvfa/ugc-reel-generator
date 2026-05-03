import streamlit as st
from huggingface_hub import InferenceClient
import edge_tts
import os
import subprocess
import time

client = InferenceClient(token=st.secrets["HF_TOKEN"])

def query_image_gen(prompt):
    model_id = "black-forest-labs/FLUX.1-schnell"
    ugc_prompt = f"{prompt}, realistic UGC style, amateur smartphone photo, candid, high resolution"
    image = client.text_to_image(ugc_prompt, model=model_id)
    if not os.path.exists("output"): os.makedirs("output")
    path = "output/base_image.png"
    image.save(path)
    return path

def query_im2im_gen(uploaded_file, prompt):
    image_bytes = uploaded_file.getvalue()
    image = client.image_to_image(
        image=image_bytes,
        prompt=f"{prompt}, high quality, realistic",
        model="lllyasviel/control_v11p_sd15_canny" 
    )
    if not os.path.exists("output"): os.makedirs("output")
    path = "output/base_image.png"
    image.save(path)
    return path

def create_ugc_video(image_path, audio_path, duration):
    output_path = "output/final_reel.mp4"
    
    # FFmpeg command: handles image with optional audio
    cmd = ['ffmpeg', '-y', '-loop', '1', '-i', image_path]
    
    if audio_path and os.path.exists(audio_path):
        cmd.extend(['-i', audio_path])
        cmd.extend(['-c:v', 'libx264', '-t', str(duration), '-pix_fmt', 'yuv420p', '-vf', 'scale=1080:1920', '-shortest', output_path])
    else:
        cmd.extend(['-c:v', 'libx264', '-t', str(duration), '-pix_fmt', 'yuv420p', '-vf', 'scale=1080:1920', output_path])
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path
    except subprocess.CalledProcessError as e:
        st.error(f"FFmpeg Error: {e.stderr.decode()}")
        return None

async def generate_voice(text, voice, output_path="output/voice.mp3"):
    if not os.path.exists("output"): os.makedirs("output")
    if os.path.exists(output_path): os.remove(output_path)
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)
    return output_path
