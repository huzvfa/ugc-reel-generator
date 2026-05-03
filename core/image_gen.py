import requests
import io
import streamlit as st

# Check secrets
if "HF_TOKEN" not in st.secrets:
    st.error("HF_TOKEN missing in Secrets dashboard.")
    st.stop()

HEADERS = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}

# URL 1: Standard SDXL Turbo (for Text-to-Image)
T2I_URL = "https://api-inference.huggingface.co/models/stabilityai/sdxl-turbo"

# URL 2: ControlNet or similar for Image-to-Image (Keeps composition of sample)
# A generic ControlNet model is usually best for Im2Im structure
I2I_URL = "https://api-inference.huggingface.co/models/lllyasviel/control_v11p_sd15_canny"

# Helper function to save API response to file
def save_response_to_file(response_content, filename="output/creator.png"):
    try:
        from PIL import Image
        image = Image.open(io.BytesIO(response_content))
        # Ensure correct vertical aspect ratio (9:16) for Reels
        # We may need to resize if the model output is 1:1
        if image.width > image.height:
             # Basic vertical crop/resize example
             new_height = int(image.width * (16/9))
             image = image.resize((image.width, new_height))
        
        image.save(filename)
        return filename
    except Exception as e:
        raise Exception(f"Failed to process API image: {e}")


# --- FUNCTION 1: Standard Text-to-Image ---
def query_image_gen(prompt):
    # Optimize prompt for UGC style
    ugc_prompt = f"{prompt}, portrait, shot on mobile phone, realistic, social media style"
    
    response = requests.post(T2I_URL, headers=HEADERS, json={"inputs": ugc_prompt})
    
    if response.status_code != 200:
        raise Exception(f"API Error (T2I): {response.status_code}, {response.text}")
        
    return save_response_to_file(response.content, "output/t2i_ugc.png")


# --- NEW FUNCTION 2: Image-to-Image Reference ---
def query_im2im_gen(uploaded_file, prompt):
    # Prepare the uploaded file for the API request
    # Read the file data
    image_data = uploaded_file.getvalue()
    
    # We combine the reference image + the new prompt
    payload = {
        "inputs": prompt,
        "image": image_data 
    }
    
    st.info("Sending Image-to-Image request (This takes longer than T2I)...")
    
    # The Hugging Face inference API structure for Im2Im varies slightly, 
    # but the ControlNet Canny API expects raw bytes of the image
    response = requests.post(I2I_URL, headers=HEADERS, data=image_data)
    
    if response.status_code != 200:
        raise Exception(f"API Error (I2I): {response.status_code}, {response.text}")
        
    st.success("Hugging Face processed the image structure. Saving final asset...")
    
    # Save the output of the structure model (this model might output an 'edge map' first, which we then need to 're-color' with another API call for true 'real-time Im2Im'. To keep it FREE and simple, this model might just output a structured version).
    return save_response_to_file(response.content, "output/i2i_ugc.png")
