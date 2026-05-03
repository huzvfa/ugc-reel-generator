import streamlit as st
import asyncio
from core import generator
import os

st.set_page_config(page_title="UGC AI Suite", layout="wide")

# --- GLASSMORPHISM & ANIMATION CSS ---
st.markdown("""
    <style>
    /* Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    
    /* Glassmorphism Container */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 25px;
    }

    /* Typing Animation for Textarea */
    @keyframes typing {
      from { width: 0 }
      to { width: 100% }
    }
    
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.03) !important;
        color: #00f2fe !important;
        border: 1px solid #4facfe !important;
        transition: 0.3s;
    }
    
    .stTextArea textarea:focus {
        box-shadow: 0 0 15px #00f2fe;
        background: rgba(255, 255, 255, 0.08) !important;
    }

    /* Custom Button */
    .stButton>button {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        border: none;
        color: white;
        font-weight: bold;
        border-radius: 12px;
        padding: 10px 30px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.6);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 UGC AI Glossy Suite")
st.markdown("Create professional reels with advanced AI voices.")

# --- 1. MODE SELECTION ---
mode = st.radio("Select Mode:", ["Text-to-Image", "Image-to-Image", "Text-to-Video", "Image-to-Video"], horizontal=True)

# --- 2. CONFIGURATION ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

if "Image-" in mode:
    uploaded_file = st.file_uploader("Upload Sample Image", type=["jpg", "png", "jpeg"])
else:
    uploaded_file = None

prompt = st.text_area("Describe your AI Scenario:", placeholder="A young entrepreneur working in a modern office in Islamabad...", help="Type your creative vision here.")

# Conditional UI for Video
if "Video" in mode:
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        video_duration = st.slider("Video Length (Seconds):", 5, 30, 15)
        add_voiceover = st.toggle("Enable AI Voiceover", value=True)
        
    with col2:
        if add_voiceover:
            script = st.text_area("Script:", "Hey everyone, welcome to my creative space!")
            
            # EXPANDED VOICE LIBRARY
            voice_options = {
                "Young Adult (Female)": "en-US-AnaNeural",
                "Young Adult (Male)": "en-US-ChristopherNeural",
                "Adult (Female)": "en-US-JennyNeural",
                "Adult (Male)": "en-US-GuyNeural",
                "Elderly (Female)": "en-US-CoraNeural",
                "Elderly (Male)": "en-US-RogerNeural",
                "British Professional (Male)": "en-GB-RyanNeural"
            }
            selected_voice = st.selectbox("Select Voice Agent:", list(voice_options.keys()))
            
            if st.button("🔊 Preview Voice"):
                with st.spinner("Wait..."):
                    p_path = asyncio.run(generator.generate_voice("This is a preview of your selected AI agent.", voice_options[selected_voice], "output/p.mp3"))
                    st.audio(p_path)

st.markdown('</div>', unsafe_allow_html=True)

# --- 3. GENERATION ---
if st.button("🚀 Generate Final Content"):
    with st.spinner("AI Processing..."):
        # Image Logic
        if "Image-" in mode and uploaded_file:
            img_path = generator.query_im2im_gen(uploaded_file, prompt)
        else:
            img_path = generator.query_image_gen(prompt)
            
        # Video/Audio Logic
        if "Video" in mode:
            audio_path = None
            if add_voiceover:
                audio_path = asyncio.run(generator.generate_voice(script, voice_options[selected_voice], "output/final.mp3"))
            
            video_path = generator.create_ugc_video(img_path, audio_path, video_duration)
            if video_path:
                st.video(video_path)
        else:
            st.image(img_path)
