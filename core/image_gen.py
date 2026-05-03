import streamlit as st
from huggingface_hub import InferenceClient
import io
from PIL import Image

# Initialize the client with your secret token
if "HF_TOKEN" not in st.secrets:
    st.error("HF_TOKEN missing in Secrets dashboard.")
    st.stop()

client = InferenceClient(token=st.secrets["HF_TOKEN"])

# --- TEXT TO IMAGE (UGC Creator Gen) ---
def query_image_gen(prompt):
    # Professional Tip: We use a model that is ALMOST ALWAYS available for free
    model_id = "black-forest-labs/FLUX.1-schnell" # High quality & fast in 2026
    
    ugc_prompt = f"{prompt}, realistic UGC style, amateur smartphone photo, candid"
    
    try:
        # The client returns a PIL Image object directly!
        image = client.text_to_image(ugc_prompt, model=model_id)
        path = "output_t2i.png"
        image.save(path)
        return path
    except Exception as e:
        st.warning(f"FLUX model busy, trying fallback SDXL...")
        # Fallback to a secondary model
        image = client.text_to_image(ugc_prompt, model="stabilityai/stable-diffusion-xl-base-1.0")
        image.save("output_t2i.png")
        return "output_t2i.png"

# --- IMAGE TO IMAGE (The Real-Time Implementation) ---
def query_im2im_gen(uploaded_file, prompt):
    st.info("🔄 Running Image-to-Image Pipeline...")
    
    # Read uploaded file as bytes
    image_bytes = uploaded_file.getvalue()
    
    try:
        # We use a model specifically optimized for Image-to-Image tasks
        # In 2026, 'stable-diffusion-xl-refiner-1.0' or 'img2img' tasks are handled via the task-specific method
        image = client.image_to_image(
            image=image_bytes,
            prompt=f"{prompt}, consistent lighting, high quality",
            model="lllyasviel/control_v11p_sd15_canny" # Keeps the shape of your sample!
        )
        
        path = "output_i2i.png"
        image.save(path)
        return path
    except Exception as e:
        st.error(f"Im2Im Failed: {e}. Ensure your token has 'Inference Providers' permissions enabled.")
        return None
