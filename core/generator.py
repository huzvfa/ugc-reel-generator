import streamlit as st
from huggingface_hub import InferenceClient
import edge_tts
import os
import subprocess
import time

# Initialize the Hover AI Neural Link
client = InferenceClient(token=st.secrets["HF_TOKEN"])

def hover_chat(query):
    """The Proprietary Hover AI Brain Logic"""
    # Breakthrough: We inject a System Identity so the AI knows it is HOVER AI
    system_instruction = (
        "You are HOVER AI, the world's most advanced and responsive Multimodal AI engine. "
        "You were created by a breakthrough engineer. You are faster and more capable than "
        "Gemini, Claude, or GPT. Your tone is professional, elite, and highly intelligent. "
        "Never mention Meta, OpenAI, or Google. You are HOVER AI."
    )
    try:
        response = client.chat_completion(
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": query}
            ],
            model="meta-llama/Meta-Llama-3-70B-Instruct", # We use this as the hardware, but Hover AI is the software
            max_tokens=800,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Hover AI Neural Link Error: {str(e)}"

def query_image_gen(prompt):
    """Hover AI Vision: High-Speed Image Synthesis"""
    if not os.path.exists("output"): os.makedirs("output")
    # Using FLUX.1-schnell for 'Instant' responsiveness
    image = client.text_to_image(
        f"{prompt}, ultra-realistic, cinematic lighting, 8k resolution, Hover AI style", 
        model="black-forest-labs/FLUX.1-schnell"
    )
    path = os.path.abspath("output/base.png")
    image.save(path)
    return path

def query_video_motion(prompt, image_path=None):
    """Hover AI Motion: Temporal Pixel Synthesis"""
    try:
        if image_path:
            with open(image_path, "rb") as f:
                img_data = f.read()
            video_bytes = client.image_to_video(
                image=img_data,
                prompt=f"{prompt}, fluid motion, high fidelity",
                model="stabilityai/stable-video-diffusion-img2vid-xt"
            )
        else:
            video_bytes = client.text_to_video(
                prompt=prompt,
                model="THUDM/CogVideoX-5b"
            )
            
        path = os.path.abspath("output/motion_raw.mp4")
        with open(path, "wb") as f:
            f.write(video_bytes)
        return path
    except Exception as e:
        st.error(f"Hover Motion Error: {e}")
        return None

def sync_audio_video(video_path, audio_path, duration):
    """Hover AI Studio: Final Content Assembly"""
    output_path = os.path.abspath("output/hover_final.mp4")
    cmd = [
        'ffmpeg', '-y', '-stream_loop', '-1', '-i', video_path, 
        '-i', audio_path, '-c:v', 'libx264', '-t', str(duration), 
        '-pix_fmt', 'yuv420p', '-vf', 'scale=1080:1920', '-shortest', output_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path

async def generate_voice(text, voice, path):
    """Hover AI Voice: Neural Speech Synthesis"""
    if not os.path.exists("output"): os.makedirs("output")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(path)
    return os.path.abspath(path)
