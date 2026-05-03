import streamlit as st
import asyncio
import subprocess  # FIXED: Added missing import
from core import generator
import os

st.set_page_config(page_title="Creatify AI Clone", layout="wide")

# --- CUSTOM CSS FOR SIDEBAR & GLOSSY INTERFACE ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #333; }
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    .card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
    }
    .stTextArea textarea { background-color: #1a1c24 !important; color: #00f2fe !important; border: 1px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("💠 Studio")
    st.button("🏠 Dashboard")
    st.button("📁 My Projects")
    st.button("🎭 Brand Kit")
    st.divider()
    st.button("🛠️ Settings")

# --- MAIN INTERFACE ---
st.title("What are you making today?")

VOICES = {
    "🇺🇸 USA - Young Female": "en-US-AnaNeural",
    "🇺🇸 USA - Mature Male": "en-US-ChristopherNeural",
    "🇬🇧 UK - Deep Male": "en-GB-RyanNeural",
    "🇵🇰 PK - Urdu Male": "ur-PK-AsadNeural",
    "🇵🇰 PK - Urdu Female": "ur-PK-UzmaNeural",
    "🇮🇳 IN - Hindi Female": "hi-IN-SwaraNeural",
    "🇦🇺 AUS - Casual Male": "en-AU-WilliamNeural",
    "🇯🇵 JPN - Soft Female": "ja-JP-NanamiNeural",
    "🇸🇦 SAU - Arabic Male": "ar-SA-HamedNeural",
    "🇩🇪 GER - Serious Male": "de-DE-ConradNeural"
}

mode = st.selectbox("Choose AI Tool:", ["Text-to-Image", "Text-to-Video", "Image-to-Image", "Image-to-Video"])

st.markdown('<div class="card">', unsafe_allow_html=True)
col1, col2 = st.columns([1.5, 1])

with col1:
    prompt = st.text_area("Describe your AI Scenario:", placeholder="A professional UGC ad for skincare...")
    
    if mode == "Image-to-Image":
        u1 = st.file_uploader("Primary Image (Scene)", type=['png','jpg'])
        u2 = st.file_uploader("Reference Image (Face/Body)", type=['png','jpg'])
    elif mode == "Image-to-Video":
        u1 = st.file_uploader("Source Image", type=['png','jpg'])
    
    if "Video" in mode:
        script = st.text_area("Script:")
        duration = st.slider("Target Length (s):", 5, 30, 15)
        voice_choice = st.selectbox("Voice Agent:", list(VOICES.keys()))
        
        if st.button("🔊 Preview Voice"):
            asyncio.run(generator.generate_voice("This is a preview.", VOICES[voice_choice], "output/p.mp3"))
            st.audio("output/p.mp3")

with col2:
    st.info("AI Status: Ready")
    if st.button("🚀 CREATE NOW", use_container_width=True):
        if not prompt:
            st.error("Please enter a description.")
        else:
            with st.spinner("AI Engine Syncing..."):
                # 1. Generate Visuals
                if mode == "Image-to-Image":
                    img_path = generator.query_im2im_gen(u1, u2, prompt)
                else:
                    img_path = generator.query_image_gen(prompt)
                
                st.image(img_path, caption="AI Base Generated")

                # 2. Handle Video
                if "Video" in mode:
                    audio_path = asyncio.run(generator.generate_voice(script, VOICES[voice_choice], "output/audio.mp3"))
                    video_path = generator.query_video_gen(img_path, prompt)
                    
                    # FFmpeg rendering if API times out or for final assembly
                    if video_path == "fallback" or video_path is None:
                        st.warning("Optimizing Video Render...")
                        final_v = "output/final_reel.mp4"
                        cmd = ['ffmpeg', '-y', '-loop', '1', '-i', img_path, '-i', audio_path, '-c:v', 'libx264', '-t', str(duration), '-pix_fmt', 'yuv420p', '-vf', 'scale=1080:1920', final_v]
                        subprocess.run(cmd, check=True)
                        st.video(final_v)
                    else:
                        st.video(video_path)
st.markdown('</div>', unsafe_allow_html=True)
