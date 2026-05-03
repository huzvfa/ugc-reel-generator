import requests
import io
import streamlit as st
from PIL import Image

# Ensure HF_TOKEN is in secrets
if "HF_TOKEN" not in st.secrets:
    st.error("HF_TOKEN missing in Streamlit Secrets!")
    st.stop()

# NEW UPDATED ROUTER URLS
T2I_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/sdxl-turbo"
I2I_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-refiner-1.0" 

HEADERS = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}

def save_response_to_file(response_content, filename):
    try:
        image = Image.open(io.BytesIO(response_content))
        # Optional: Force 9:16 aspect ratio for Reels
        image.save(filename)
        return filename
    except Exception as e:
        raise Exception(f"Failed to decode image: {e}")

# --- TEXT TO IMAGE ---
def query_image_gen(prompt):
    payload = {"inputs": f"{prompt}, realistic UGC style, shot on phone, 4k"}
    response = requests.post(T2I_URL, headers=HEADERS, json=payload)
    
    if response.status_code != 200:
        # If SDXL Turbo is down/busy, try a fallback model
        st.warning("Primary model busy, trying fallback...")
        fallback_url = "https://router.huggingface.co/hf-inference/models/runwayml/stable-diffusion-v1-5"
        response = requests.post(fallback_url, headers=HEADERS, json=payload)

    if response.status_code == 200:
        return save_response_to_file(response.content, "output_t2i.png")
    else:
        raise Exception(f"API Error {response.status_code}: {response.text}")

# --- IMAGE TO IMAGE ---
def query_im2im_gen(uploaded_file, prompt):
    # Convert uploaded file to bytes
    image_bytes = uploaded_file.getvalue()
    
    # Hugging Face Im2Im expectation:
    # Some models take JSON with base64, others take raw binary + parameters in headers
    # For the Router API, we send the image as raw data.
    
    st.info("Sending reference image to AI...")
    response = requests.post(
        I2I_URL, 
        headers=HEADERS, 
        data=image_bytes, # Raw image data
        params={"inputs": prompt} # Prompt as a parameter
    )
    
    if response.status_code == 200:
        return save_response_to_file(response.content, "output_i2i.png")
    else:
        # Fallback for Im2Im
        st.error(f"Im2Im Failed ({response.status_code}). Try Text-to-Image instead.")
        return None
