import streamlit as st
from huggingface_hub import InferenceClient
import edge_tts
import os
from PIL import Image
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

client = InferenceClient(token=st.secrets["HF_TOKEN"])

def query_image_gen(prompt):
    # Flux is the best free model currently available
    model_id = "black-forest-labs/FLUX.1-schnell"
    ugc_prompt = f"{prompt}, realistic UGC style, amateur smartphone photo, candid"
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

# --- NEW: 30-Second Video Engine (The "UGC Fix") ---
def create_ugc_video(image_path, audio_path, duration):
    try:
        # Load the generated AI image and voiceover
        img_clip = ImageClip(image_path).set_duration(duration)
        audio_clip = AudioFileClip(audio_path)
        
        # Ensure audio and video length match
        final_duration = min(duration, audio_clip.duration + 1)
        video = img_clip.set_duration(final_duration).set_audio(audio_clip)
        
        # Apply a 'Ken Burns' effect (Slow Zoom) to make it feel like a video
        video = video.resize(lambda t: 1 + 0.02 * t) # Subtle 2% zoom over time
        
        output_path = "output/final_reel.mp4"
        video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
        return output_path
    except Exception as e:
        st.error(f"Video Rendering Error: {e}")
        return None

async def generate_voice(text, voice, output_path="output/voice.mp3"):
    if not os.path.exists("output"): os.makedirs("output")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)
    return output_path
