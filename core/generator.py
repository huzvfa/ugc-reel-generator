import streamlit as st
from huggingface_hub import InferenceClient
import edge_tts
import os
import subprocess

client = InferenceClient(token=st.secrets["HF_TOKEN"])

def hover_visual_gen(prompt, mode, u1=None):
    """Proprietary Vision: FLUX.1 with secondary cluster failover."""
    if not os.path.exists("output"): os.makedirs("output")
    path = os.path.abspath("output/hover_vision.png")
    enhanced_p = f"{prompt}, hyper-realistic, 8k, cinematic, raw detail"

    try:
        if mode == "Image-to-Image" and u1:
            img = client.image_to_image(image=u1.getvalue(), prompt=enhanced_p, model="lllyasviel/control_v11p_sd15_canny")
        else:
            # Primary: FLUX Dev for maximum quality
            img = client.text_to_image(enhanced_p, model="black-forest-labs/FLUX.1-dev")
        img.save(path)
        return path
    except:
        # Failover: Schnell for high speed
        img = client.text_to_image(enhanced_p, model="black-forest-labs/FLUX.1-schnell")
        img.save(path)
        return path

def hover_video_gen(prompt, base_img, duration):
    """Temporal Synthesis: 9:16 Vertical Video Mastering."""
    final_v = os.path.abspath("output/hover_final.mp4")
    try:
        with open(base_img, "rb") as f:
            img_data = f.read()
        video_bytes = client.image_to_video(img_data, model="stabilityai/stable-video-diffusion-img2vid-xt")
        temp_v = os.path.abspath("output/temp.mp4")
        with open(temp_v, "wb") as f:
            f.write(video_bytes)
        # Professional 9:16 Crop for TikTok/Reels
        cmd = ['ffmpeg', '-y', '-stream_loop', '-1', '-i', temp_v, '-t', str(duration), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920', final_v]
        subprocess.run(cmd, check=True, capture_output=True)
        return final_v
    except:
        return None

async def hover_voice_engine(text, voice, tone):
    """Tone-Modulated Neural Speech."""
    path = os.path.abspath("output/voice.mp3")
    map = {"Seductive": {"p": "-10Hz", "r": "-15%"}, "Serious": {"p": "-5Hz", "r": "-10%"}, "Soft": {"p": "+0Hz", "r": "-5%"}}
    t = map.get(tone, {"p": "+0Hz", "r": "+0%"})
    communicate = edge_tts.Communicate(text, voice, pitch=t.get("p", "+0Hz"), rate=t.get("r", "+0%"))
    await communicate.save(path)
    return path
