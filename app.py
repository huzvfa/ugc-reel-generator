import streamlit as st
import asyncio
from core import generator
import os

# --- UI STYLING ---
st.set_page_config(page_title="UGC AI Suite", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    .neon-box {
        border: 1px solid #00f2fe; padding: 20px; border-radius: 15px;
        box-shadow: 0 0 15px rgba(0,242,254,0.1); margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 UGC AI Content Creator")

# --- 1. CONFIGURATION ---
mode = st.radio("Generation Mode:", ["Text-to-Image", "Image-to-Image", "Text-to-Video", "Image-to-Video"], horizontal=True)

with st.container():
    st.markdown('<div class="neon-box">', unsafe_allow_html=True)
    
    uploaded_file = None
    if "Image-" in mode:
        uploaded_file = st.file_uploader("Upload reference photo...", type=["jpg", "png", "jpeg"])
    
    prompt = st.text_area("Describe your AI Scenario:", placeholder="A person showing a product in a modern cafe...")
    
    # Conditional Video Options
    if "Video" in mode:
        col1, col2 = st.columns(2)
        with col1:
            script = st.text_area("Video Script:", "Check out this amazing find! Link in bio.")
            video_duration = st.slider("Target Length (Seconds):", 5, 30, 15)
        with col2:
            voices = {"Male (Pro)": "en-US-ChristopherNeural", "Female (Energetic)": "en-US-AnaNeural"}
            selected_voice = st.selectbox("Select Voice Agent:", list(voices.keys()))
            if st.button("🔊 Preview Voice"):
                p_path = asyncio.run(generator.generate_voice("This is your AI agent voice.", voices[selected_voice], "output/p.mp3"))
                st.audio(p_path)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 2. EXECUTION ---
if st.button("🚀 Generate Final Content"):
    if ("Image-" in mode) and uploaded_file is None:
        st.error("Please upload an image for this mode!")
    else:
        with st.spinner("AI Engine Processing..."):
            # Step A: Image Generation
            if "Image-" in mode:
                img_path = generator.query_im2im_gen(uploaded_file, prompt)
            else:
                img_path = generator.query_image_gen(prompt)
            
            # Step B: Video/Audio Logic
            if "Video" in mode:
                audio_path = asyncio.run(generator.generate_voice(script, voices[selected_voice], "output/final.mp3"))
                video_path = generator.create_ugc_video(img_path, audio_path, video_duration)
                
                if video_path:
                    st.video(video_path)
                    st.success("30-Second AI Reel Generated!")
            else:
                st.image(img_path, caption="Generated UGC Image", use_column_width=True)
