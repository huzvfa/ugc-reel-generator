import streamlit as st
from huggingface_hub import InferenceClient
import edge_tts
import os
import subprocess

client = InferenceClient(token=st.secrets["HF_TOKEN"])

def hover_visual_gen(prompt, mode, u1=None):
    if not os.path.exists("output"): os.makedirs("output")
    path = os.path.abspath("output/hover_vision.png")
    enhanced_p = f"{prompt}, hyper-realistic, 8k, cinematic, raw detail"

    try:
        # Standardizing on Schnell for unlimited high-speed free tier usage
        img = client.text_to_image(
            enhanced_p, 
            model="black-forest-labs/FLUX.1-schnell",
            headers={"x-use-cache": "false"} # Force fresh generation
        )
        img.save(path)
        return path
    except:
        # Emergency Fallback to Stable Diffusion XL
        img = client.text_to_image(enhanced_p, model="stabilityai/stable-diffusion-xl-base-1.0")
        img.save(path)
        return path

# (hover_video_gen and hover_voice_engine remain operational)
