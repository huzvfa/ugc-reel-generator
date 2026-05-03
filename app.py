import streamlit as st
import asyncio
from core import generator

# Glossy UI CSS
st.set_page_config(page_title="UGC AI Pro", layout="wide")
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63); color: white; }
    .glass { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 25px; border: 1px solid rgba(255,255,255,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 UGC AI Glossy Studio")

# 1. RESTORED MODES
mode = st.radio("Select Mode:", ["Text-to-Image", "Text-to-Video", "Image-to-Image", "Image-to-Video"], horizontal=True)

with st.container():
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    
    # Mode-Specific Uploaders
    if mode == "Image-to-Image":
        col_img1, col_img2 = st.columns(2)
        with col_img1: img1 = st.file_uploader("Primary Image (Scene/Pose)", type=["jpg", "png"])
        with col_img2: img2 = st.file_uploader("Reference Image (Face/Body)", type=["jpg", "png"])
    elif mode == "Image-to-Video":
        img1 = st.file_uploader("Upload Image to Animate", type=["jpg", "png"])
    
    prompt = st.text_area("Describe Scenario/Motion:")

    # Voice & Script Options
    if "Video" in mode:
        st.markdown("---")
        script = st.text_area("Script (Voice requires this):")
        duration = st.slider("Video Length:", 5, 30, 15)
        
        # PRO VOICE LIBRARY (Accents & Urdu)
        voices = {
            "USA - Young (Female)": "en-US-AnaNeural",
            "UK - Mature (Male)": "en-GB-RyanNeural",
            "Pakistani - English (Male)": "en-PK-AsadNeural",
            "Indian - Soft (Female)": "en-IN-NeerjaNeural",
            "Urdu - Professional (Male)": "ur-PK-AsadNeural",
            "Urdu - Sweet (Female)": "ur-PK-UzmaNeural"
        }
        selected_voice = st.selectbox("Select Voice Agent:", list(voices.keys()))
    st.markdown('</div>', unsafe_allow_html=True)

if st.button("🚀 Generate Content"):
    with st.spinner("Executing AI Pipeline..."):
        # Image Handling
        if mode == "Image-to-Image":
            img_path = generator.query_im2im_gen(img1, img2, prompt)
        elif mode == "Image-to-Video" or mode == "Text-to-Video":
            # For Video, generate/use image base first
            img_path = generator.query_image_gen(prompt) if mode == "Text-to-Video" else "output/base.png" # Assuming upload saved
        else:
            img_path = generator.query_image_gen(prompt)

        # Video Handling
        if "Video" in mode:
            audio_path = asyncio.run(generator.generate_voice(script, voices[selected_voice]))
            motion_path = generator.query_video_gen(img_path, prompt)
            
            if motion_path and audio_path:
                final_reel = generator.assemble_reel(motion_path, audio_path, duration)
                st.video(final_reel)
        else:
            st.image(img_path)
