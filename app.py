import streamlit as st
import asyncio
from core import generator
import os

st.set_page_config(page_title="UGC AI Suite", layout="wide")

# Modern Neon Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        background: linear-gradient(45deg, #00f2fe 0%, #4facfe 100%);
        border: none; color: white; box-shadow: 0 0 15px rgba(0,242,254,0.4);
    }
    .neon-box {
        border: 1px solid #00f2fe; padding: 20px; border-radius: 15px;
        box-shadow: 0 0 10px rgba(0,242,254,0.1); margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 UGC AI Reel Generator")

# 1. Upload Section
with st.container():
    st.markdown('<div class="neon-box">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload reference photo...", type=["jpg", "png", "jpeg"])
    st.markdown('</div>', unsafe_allow_html=True)

# 2. Configuration
st.header("2. Configure Generator")
col1, col2 = st.columns([1.5, 1])

with col2:
    mode = st.radio("Generation Mode:", ["Text-to-Image", "Image-to-Image", "Text-to-Video", "Image-to-Video"])

with col1:
    prompt = st.text_area("Describe your AI Scenario:", placeholder="A person talking to the camera...")
    
    # --- CONDITIONAL UI ---
    if "Video" in mode:
        st.markdown("---")
        script = st.text_area("Script (Text to Speech):", "Check out this amazing product!")
        video_duration = st.slider("Target Video Length (Seconds):", 5, 30, 15)
        
        voices = {
            "Male (Professional)": "en-US-ChristopherNeural",
            "Female (Energetic)": "en-US-AnaNeural"
        }
        selected_voice = st.selectbox("Select Voiceover Agent:", list(voices.keys()))
        
        if st.button("🔊 Preview Voice"):
            p_path = asyncio.run(generator.generate_voice("Testing the agent.", voices[selected_voice], "output/p.mp3"))
            st.audio(p_path)

# 3. Execution
if st.button("🚀 Generate Final Content"):
    with st.spinner("Executing AI Pipeline..."):
        # Image Logic
        if "Image-to" in mode or "Image-Video" in mode:
            if not uploaded_file: st.error("Upload an image first!"); st.stop()
            img_path = generator.query_im2im_gen(uploaded_file, prompt)
        else:
            img_path = generator.query_image_gen(prompt)
        
        st.image(img_path, caption="Base Image Generated", width=300)

        # Video Logic
        if "Video" in mode:
            audio_path = asyncio.run(generator.generate_voice(script, voices[selected_voice], "output/final.mp3"))
            video_path = generator.query_video_gen(img_path)
            
            if video_path:
                st.success(f"Video clip generated! Use MoviePy to loop to {video_duration}s.")
                st.video(video_path)
                st.audio(audio_path)
