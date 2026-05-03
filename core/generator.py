import streamlit as st
from huggingface_hub import InferenceClient
import edge_tts
import os
import time

client = InferenceClient(token=st.secrets["HF_TOKEN"])

def query_image_gen(prompt):
    image = client.text_to_image(f"{prompt}, realistic ugc, 4k", model="black-forest-labs/FLUX.1-schnell")
    if not os.path.exists("output"): os.makedirs("output")
    path = os.path.abspath("output/base.png")
    image.save(path)
    return path

def query_im2im_gen(u1, u2, prompt):
    if not os.path.exists("output"): os.makedirs("output")
    img = client.image_to_image(image=u1.getvalue(), prompt=prompt, model="lllyasviel/control_v11p_sd15_canny")
    path = os.path.abspath("output/im2im.png")
    img.save(path)
    return path

async def generate_voice(text, voice, path):
    if not os.path.exists("output"): os.makedirs("output")
    if os.path.exists(path): os.remove(path)
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(path)
    # Wait to ensure file is closed by system
    time.sleep(1) 
    return os.path.abspath(path)
