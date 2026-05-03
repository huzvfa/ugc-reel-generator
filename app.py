import streamlit as st
import asyncio
from core import generator
import os

st.set_page_config(page_title="Creatify AI Clone", layout="wide")

# --- CUSTOM CSS FOR SIDEBAR & GLOSSY INTERFACE ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #333; }
    .stApp { background-color: #0b0e14; }
    .card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        transition: transform 0.3s ease;
    }
    .card:hover { transform: translateY(-5px); border-color: #4facfe; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (Creatify Style) ---
with st.sidebar:
    st.title("🚀 Studio")
    st.button("🏠 Home")
    st.button("📁 Projects")
    st.button("🎭 My Brand")
    st.divider()
    st.caption("Advanced Tools")
    st.button("⚙️ API")

# --- MAIN INTERFACE ---
st.title("What are you making today?")

# --- 15+ VOICE LIBRARY WITH ACCENTS ---
VOICES = {
    "🇺🇸 USA - Young Female": "en-US-AnaNeural",
    "🇺🇸 USA - Mature Male": "en-US-ChristopherNeural",
    "🇬🇧 UK - Elegant Female": "en-GB-SoniaNeural",
    "🇬🇧 UK - Deep Male": "en-GB-RyanNeural",
    "🇵🇰 PK - Urdu Male": "ur-PK-AsadNeural",
    "🇵🇰 PK - Urdu Female": "ur-PK-UzmaNeural",
    "🇮🇳 IN - Hindi/Eng Female": "en-IN-NeerjaNeural",
    "🇩🇪 GER - Serious Male": "de-DE-ConradNeural",
    "🇦🇺 AUS - Casual Male": "en-AU-WilliamNeural",
    "🇫🇷 FRA - Soft Female": "fr-FR-DeniseNeural",
    "🇸🇦 SAU - Arabic Male": "ar-SA-HamedNeural",
    "🇪🇸 ESP - Sharp Female": "es-ES-ElviraNeural",
    "🇯🇵 JPN - Anime Style": "ja-JP-NanamiNeural",
    "🇺🇸 USA - Kid Voice": "en-US-GuyNeural", # Modulated via script
    "🇬🇧 UK - Mature Lady": "en-GB-LibbyNeural"
}

mode = st.selectbox("Select Tool:", ["Text-to-Image", "Text-to-Video", "Image-to-Image", "Image-to-Video"])

# Dynamic Cards for Modes
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    prompt = st.text_area("Describe your Vision (AI Scenario):", placeholder="An aesthetic UGC ad for a skincare brand...")
    
    if "Image-to-Image" in mode:
        c1, c2 = st.columns(2)
        u1 = c1.file_uploader("Upload Scene", type=['png','jpg'])
        u2 = c2.file_uploader("Upload Face/Body Ref", type=['png','jpg'])
    elif "Image-to-Video" in mode:
        u1 = st.file_uploader("Upload Source Image", type=['png','jpg'])
        
    if "Video" in mode:
        script = st.text_area("Script for AI Actor:")
        duration = st.slider("Duration", 5, 30, 15)
        voice_choice = st.selectbox("Select Voiceover Agent:", list(VOICES.keys()))
        
        # --- REAL-TIME VOICE PREVIEW ---
        if st.button("🔊 Preview Voice"):
            v_path = "output/preview.mp3"
            asyncio.run(generator.generate_voice("Testing this premium voice agent.", VOICES[voice_choice], v_path))
            st.audio(v_path)
    st.markdown('</div>', unsafe_allow_html=True)

# --- EXECUTION ENGINE ---
if st.button("🚀 CREATE NOW"):
    with st.spinner("AI Engine Syncing..."):
        # 1. Faster Image Generation
        if mode == "Image-to-Image":
            img_path = generator.query_im2im_gen(u1, u2, prompt)
        else:
            img_path = generator.query_image_gen(prompt)
        
        # 2. Advanced Video Logic
        if "Video" in mode:
            audio_path = asyncio.run(generator.generate_voice(script, VOICES[voice_choice], "output/audio.mp3"))
            video_path = generator.query_video_gen(img_path, prompt)
            
            if video_path == "fallback":
                # Create high-quality dynamic video if API is busy
                cmd = ['ffmpeg', '-y', '-loop', '1', '-i', img_path, '-i', audio_path, '-c:v', 'libx264', '-t', str(duration), '-pix_fmt', 'yuv420p', '-vf', 'scale=1080:1920', 'output/final.mp4']
                subprocess.run(cmd, check=True)
                st.video("output/final.mp4")
            else:
                st.video(video_path)
        else:
            st.image(img_path)
