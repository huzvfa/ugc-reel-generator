import streamlit as st
import PIL.Image as Image # To handle uploaded images
from core import image_gen # Change import style
from core.voice_gen import generate_voiceover

st.set_page_config(page_title="UGC AI Reel Generator", layout="wide")

st.title("🎬 UGC AI Reel Generator")
st.markdown("---")

# --- Sidebar (Configuration) ---
st.sidebar.header("Configuration")
hf_token_status = "✅ Configured" if "HF_TOKEN" in st.secrets else "❌ Missing!"
st.sidebar.info(f"Hugging Face Token: {hf_token_status}")

# --- NEW: Image-to-Image Section ---
st.header("1. Upload Sample Image")
st.write("The AI engine will use this as a reference for your new image.")
uploaded_file = st.file_uploader("Choose a JPG/PNG...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Preview the uploaded image
    sample_image = Image.open(uploaded_file)
    st.image(sample_image, caption="Sample Reference", width=300)

# --- Generator Section ---
st.header("2. Configure Generator")
col1, col2 = st.columns(2)

with col1:
    prompt = st.text_area("Describe your AI Creator/Scenario:", "A young creator in a cafe talking to camera")
    script = st.text_area("Script (What they say):", "Hey guys! Check out this awesome new place, link in bio!")

with col2:
    mode = st.radio("Generation Mode:", ("Pure Text-to-Image", "Image-to-Image Reference"))

# --- Execution Section ---
st.markdown("---")
if st.button("Generate Reel Assets"):
    
    # 1. Image Generation
    with st.spinner("Analyzing reference & generating new UGC image..."):
        try:
            # We must use the updated 'image_gen.query_image_gen'
            if mode == "Image-to-Image Reference" and uploaded_file is not None:
                # Need specific logic in core/image_gen.py for this
                img_path = image_gen.query_im2im_gen(uploaded_file, prompt)
            else:
                # Text-to-Image
                img_path = image_gen.query_image_gen(prompt)
            
            st.image(img_path, caption="Generated UGC Creator (Final)", width=300)
            st.session_state['gen_img_path'] = img_path # Save for next steps

        except Exception as e:
            st.error(f"Image Generation Failed: {e}")
            st.stop()

    # 2. Voiceover Generation
    with st.spinner("Generating audio script..."):
        try:
            audio_path = generate_voiceover(script)
            st.audio(audio_path)
            st.session_state['gen_audio_path'] = audio_path
        except Exception as e:
            st.error(f"Voiceover Failed: {e}")

    st.success("Assets Generated! Ready for final assembly (Requires GPU for Animation/Editing).")
