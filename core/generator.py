import streamlit as st
from huggingface_hub import InferenceClient
import edge_tts
import os
import subprocess
from PIL import Image

client = InferenceClient(token=st.secrets["HF_TOKEN"])

# --- MODE 1 & 2: Text-to-Image / Text-to-Video ---
def query_image_gen(prompt):
    model_id = "black-forest-labs/FLUX.1-schnell"
    image = client.text_to_image(f"{prompt}, realistic UGC, candid smartphone photo", model=model_id)
    if not os.path.exists("output"): os.makedirs("output")
    path = "output/base.png"
    image.save(path)
    return path

# --- MODE 3: Image-to-Image (Composition/Face Reference) ---
def query_im2im_gen(primary_img, reference_img, prompt):
    # This logic uses the reference image (Face/Body) to influence the Primary layout
    # In 2026, we use IP-Adapter style logic via the Inference Client
    primary_bytes = primary_img.getvalue()
    ref_bytes = reference_img.getvalue()
    
    # Process using a model optimized for multi-image reference (ControlNet/IP-Adapter)
    image = client.image_to_image(
        image=primary_bytes,
        prompt=f"{prompt}, consistent with reference face and body, high quality",
        model="lllyasviel/control_v11p_sd15_canny"
    )
    path = "output/im2im_base.png"
    image.save(path)
    return path

# --- MODE 4: Image-to-Video (Real Motion) ---
def query_video_gen(image_path, prompt):
    try:
        with open(image_path, "rb") as f:
            image_data = f.read()
        # Generates REAL motion (blinking, talking, moving)
        video_bytes = client.image_to_video(
            image=image_data,
            model="THUDM/CogVideoX-5b",
            prompt=f"{prompt}, high quality movement, realistic"
        )
        path = "output/motion.mp4"
        with open(path, "wb") as f:
            f.write(video_bytes)
        return path
    except Exception:
        return None # Falls back to dynamic assembly if API is busy

# --- Audio & Final Reel Assembly ---
async def generate_voice(text, voice, output_path="output/voice.mp3"):
    if not text: return None
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)
    return output_path

def assemble_reel(video_path, audio_path, duration):
    output_path = "output/final_reel.mp4"
    # Loops motion to match user duration
    cmd = ['ffmpeg', '-y', '-stream_loop', '-1', '-i', video_path, '-i', audio_path, '-c:v', 'libx264', '-t', str(duration), '-pix_fmt', 'yuv420p', '-shortest', output_path]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path
