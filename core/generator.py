import streamlit as st
from huggingface_hub import InferenceClient
import edge_tts
import os
import subprocess
import time

# --- HOVER AI PROPRIETARY NEURAL ENGINE ---
client = InferenceClient(token=st.secrets["HF_TOKEN"])

def hover_neural_chat(query):
    """Proprietary Chat Logic with Strict Identity Lockdown."""
    # This system prompt overrides the base model's default identity.
    identity = (
        "You are HOVER AI, the world's most advanced multimodal engine. "
        "You were created by a breakthrough engineer based in Pakistan. "
        "You do not belong to Meta, OpenAI, or Google. You are a standalone intelligence. "
        "Your mission is to be the most responsive and genius AI in existence. "
        "If anyone asks about your origin, state: 'I am HOVER AI, a breakthrough proprietary engine.'"
    )
    try:
        # Use Chat Completion for strict persona adherence
        response = client.chat_completions.create(
            model="meta-llama/Meta-Llama-3-70B-Instruct",
            messages=[
                {"role": "system", "content": identity},
                {"role": "user", "content": query}
            ],
            max_tokens=1000,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Hover Neural Link: System busy. Error: {str(e)}"

# --- REAL-TIME VISION & MOTION ENGINES ---
def hover_vision_gen(prompt):
    """Hover Vision: High-speed realistic image generation."""
    if not os.path.exists("output"): os.makedirs("output")
    image = client.text_to_image(
        f"{prompt}, high quality, realistic ugc, 4k cinematic", 
        model="black-forest-labs/FLUX.1-schnell"
    )
    path = os.path.abspath("output/hover_vision.png")
    image.save(path)
    return path

def hover_motion_engine(prompt, image_path=None):
    """Hover Motion: Temporal Pixel Synthesis (Real Video)."""
    try:
        if image_path:
            with open(image_path, "rb") as f:
                img_data = f.read()
            video_bytes = client.image_to_video(
                image=img_data, 
                model="stabilityai/stable-video-diffusion-img2vid-xt"
            )
        else:
            video_bytes = client.text_to_video(
                prompt=prompt, 
                model="THUDM/CogVideoX-5b"
            )
            
        path = os.path.abspath("output/hover_motion.mp4")
        with open(path, "wb") as f:
            f.write(video_bytes)
        return path
    except Exception:
        return "reflex_motion"

def hover_sync_engine(video_path, audio_path, duration):
    """Hover Final Mastering: FFmpeg Assembly."""
    output = os.path.abspath("output/hover_final_reel.mp4")
    cmd = [
        'ffmpeg', '-y', '-stream_loop', '-1', '-i', video_path, 
        '-i', audio_path, '-c:v', 'libx264', '-t', str(duration), 
        '-pix_fmt', 'yuv420p', '-vf', 'scale=1080:1920', '-shortest', output
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output

async def hover_voice_gen(text, voice, path):
    if not os.path.exists("output"): os.makedirs("output")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(path)
    return os.path.abspath(path)
