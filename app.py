import streamlit as st
import asyncio
from core import generator
import os

st.set_page_config(page_title="UGC AI Suite", layout="wide")

# Neon Styling
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    .neon-box { border: 1px solid #00f2fe; padding: 20px; border-radius: 15px; box-shadow: 0 0 15px rgba(0,242,254,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 UGC AI Content Creator")

mode = st.radio("Generation Mode:", ["Text-to-Image", "Image-to-Image", "Text-to-Video", "Image-to-Video"], horizontal=True)

with st.container():
    st.markdown('<div class="neon-box">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload reference photo...", type=["jpg", "png", "jpeg"]) if "Image-" in mode else None
    prompt = st.text_area("Describe your AI Scenario:", placeholder="A person in a cafe...")
    
    if "Video" in mode:
        col1, col2 = st.columns(2)
        with col1:
            script = st.text_area("Video Script:", "Check out this amazing find!")
            video_duration = st.slider("Target Length (Seconds):", 5, 30, 15)
        with col2:
            voices = {"Male": "en-US-ChristopherNeural", "Female": "en-US-AnaNeural"}
            selected_voice = st.selectbox("Select Voice:", list(voices.keys()))
            if st.button("🔊 Preview Voice"):
                asyncio.run(generator.generate_voice("Testing.", voices[selected_voice], "output/p.mp3"))
                st.audio("output/p.mp3")
    st.markdown('</div>', unsafe_allow_html=True)

if st.button("🚀 Generate Final Content"):
    with st.spinner("AI Processing..."):
        if "Image-" in mode and not uploaded_file:
            st.error("Upload an image!"); st.stop()
            
        img_path = generator.query_im2im_gen(uploaded_file, prompt) if "Image-" in mode else generator.query_image_gen(prompt)
        
        if "Video" in mode:
            audio_path = asyncio.run(generator.generate_voice(script, voices[selected_voice], "output/final.mp3"))
            video_path = generator.create_ugc_video(img_path, audio_path, video_duration)
            if video_path:
                st.video(video_path)
        else:
            st.image(img_path)
