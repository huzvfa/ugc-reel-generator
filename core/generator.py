import streamlit as st
from huggingface_hub import InferenceClient
import edge_tts
import os
import subprocess
import time

# Brain of Hover AI
client = InferenceClient(token=st.secrets["HF_TOKEN"])

def hover_chat(query):
    """Elite Chat Logic - Fixed for 2026 Inference Provider Mapping"""
    try:
        # Using chat_completion is more robust than text_generation
        response = client.chat_completion(
            messages=[{"role": "user", "content": query}],
            model="meta-llama/Meta-Llama-3-70B-Instruct",
            max_tokens=500,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Hover AI Brain Error: {str(e)}"

def query_video_motion(prompt, image_path=None):
    """Generates ACTUAL AI Video Motion (CogVideoX)"""
    try:
        if image_path:
            with open(image_path, "rb") as f:
                img_data = f.read()
            # 2026 Task-specific method for Image-to-Video
            video_bytes = client.image_to_video(
                image=img_data,
                prompt=f"{prompt}, high quality movement",
                model="THUDM/CogVideoX-5b"
            )
        else:
            # Text-to-Video
            video_bytes = client.text_to_video(
                prompt=prompt,
                model="THUDM/CogVideoX-5b"
            )
            
        if not os.path.exists("output"): os.makedirs("output")
        path = os.path.abspath("output/motion_raw.mp4")
        with open(path, "wb") as f:
            f.write(video_bytes)
        return path
    except Exception as e:
        st.error(f"Motion Engine Error: {e}")
        return None

def sync_audio_video(video_path, audio_path, duration):
    """FFmpeg Sync for Hover AI Studio"""
    output_path = os.path.abspath("output/hover_final.mp4")
    # Using 'stream_loop' to ensure motion covers the full script duration
    cmd = [
        'ffmpeg', '-y', '-stream_loop', '-1', '-i', video_path, 
        '-i', audio_path, '-c:v', 'libx264', '-t', str(duration), 
        '-pix_fmt', 'yuv420p', '-vf', 'scale=1080:1920', '-shortest', output_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path
