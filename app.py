import streamlit as st
import asyncio
import subprocess
import os
from core import generator

st.set_page_config(page_title="Creatify Studio", layout="wide")

# --- CUSTOM CSS: Glossy UI & Hover Audio Hack ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px; padding: 25px;
    }
    /* Simple CSS Tooltip/Hover Effect */
    .voice-item:hover { color: #00f2fe; cursor: pointer; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("💠 Studio")
    st.button("🏠 Dashboard")
    st.button("📁 Projects")

st.title("What are you making today?")

VOICES = {
    "🇺🇸 USA Female": "en-US-AnaNeural",
    "🇺🇸 USA Male": "en-US-ChristopherNeural",
    "🇵🇰 PK Urdu Male": "ur-PK-AsadNeural",
    "🇵🇰 PK Urdu Female": "ur-PK-UzmaNeural",
    "🇬🇧 UK Male": "en-GB-RyanNeural",
    "🇮🇳 IN Female": "hi-IN-SwaraNeural"
}

mode = st.selectbox("Choose AI Tool:", ["Text-to-Image", "Text-to-Video", "Image-to-Image", "Image-to-Video"])

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
col1, col2 = st.columns([1.5, 1])

with col1:
    prompt = st.text_area("Describe Scenario:")
    
    if mode == "Image-to-Image":
        u1 = st.file_uploader("Base Image", type=['png','jpg'])
        u2 = st.file_uploader("Face Reference", type=['png','jpg'])
    
    if "Video" in mode:
        st.markdown("---")
        # OPTION: SCRIPT VS NO SCRIPT
        use_script = st.toggle("Include Voiceover & Script", value=True)
        
        if use_script:
            script = st.text_area("Script Content:")
            duration = st.slider("Length (s):", 5, 30, 10)
            
            # VOICE SELECTION
            v_choice = st.selectbox("Select Voice Agent:", list(VOICES.keys()))
            
            # HOVER PREVIEW LOGIC
            st.caption("💡 Tip: To hear a preview, click the play button below before generating.")
            if st.button("▶️ Test Selected Voice"):
                with st.spinner(""):
                    t_path = "output/preview.mp3"
                    asyncio.run(generator.generate_voice("Sample voice preview.", VOICES[v_choice], t_path))
                    st.audio(t_path)

with col2:
    if st.button("🚀 CREATE NOW", use_container_width=True):
        with st.spinner("Syncing Engine..."):
            # 1. Image Base
            if mode == "Image-to-Image":
                img_path = generator.query_im2im_gen(u1, u2, prompt)
            else:
                img_path = generator.query_image_gen(prompt)
            
            st.image(img_path)

            # 2. Video Rendering (The Fix)
            if "Video" in mode:
                final_v = os.path.abspath("output/final_reel.mp4")
                
                if use_script and script:
                    audio_path = asyncio.run(generator.generate_voice(script, VOICES[v_choice], "output/audio.mp3"))
                    # FFmpeg command with explicit absolute paths to prevent CalledProcessError
                    cmd = ['ffmpeg', '-y', '-loop', '1', '-i', img_path, '-i', audio_path, 
                           '-c:v', 'libx264', '-t', str(duration), '-pix_fmt', 'yuv420p', 
                           '-vf', 'scale=1080:1920', '-shortest', final_v]
                else:
                    # Silent video if no script
                    cmd = ['ffmpeg', '-y', '-loop', '1', '-i', img_path, 
                           '-c:v', 'libx264', '-t', '10', '-pix_fmt', 'yuv420p', 
                           '-vf', 'scale=1080:1920', final_v]
                
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                    st.video(final_v)
                except subprocess.CalledProcessError as e:
                    st.error(f"Render Error: {e.stderr}")
st.markdown('</div>', unsafe_allow_html=True)
