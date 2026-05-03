import streamlit as st
import asyncio
from core import generator

st.set_page_config(page_title="UGC AI Pro", layout="wide")

# --- EXPANDED VOICE LIBRARY ---
# Note: Styles like 'Seductive' are mapped to 'Whispering/Soft'
VOICES = {
    "USA - Professional (Male)": "en-US-GuyNeural",
    "USA - Energetic (Female)": "en-US-AnaNeural",
    "UK - Elegant (Female)": "en-GB-SoniaNeural",
    "UK - Serious (Male)": "en-GB-RyanNeural",
    "Pakistani - English Accent (Male)": "en-PK-AsadNeural",
    "Indian - Soft (Female)": "en-IN-NeerjaNeural",
    "German - Deep (Male)": "de-DE-ConradNeural",
    "Urdu - Mature (Male)": "ur-PK-AsadNeural",
    "Urdu - Sweet (Female)": "ur-PK-UzmaNeural"
}

st.title("🎬 Pro UGC AI Studio")

# Glassmorphism CSS (Simplified for speed)
st.markdown("<style>.stTextArea textarea { border: 2px solid #00f2fe; }</style>", unsafe_allow_html=True)

mode = st.radio("Mode:", ["Image-to-Video", "Text-to-Video"])
prompt = st.text_area("Describe the MOTION you want (e.g., 'The woman smiles and waves'):")

if "Video" in mode:
    col1, col2 = st.columns(2)
    with col1:
        add_voice = st.toggle("Add Voiceover", value=True)
        video_len = st.slider("Length:", 5, 30, 10)
    with col2:
        if add_voice:
            script = st.text_area("Script (Voice won't play without this):")
            voice_choice = st.selectbox("Voice & Accent:", list(VOICES.keys()))
            style = st.selectbox("Talking Style:", ["Calm", "Serious", "Angry", "Soft/Seductive", "Party", "Kid"])

if st.button("🚀 Generate Motion Reel"):
    with st.spinner("Step 1: Generating Image..."):
        img_path = generator.query_image_gen(prompt)
    
    with st.spinner("Step 2: Generating AI Motion..."):
        motion_path = generator.query_video_gen(img_path, prompt)
        # If API is busy, it falls back to zoom in generator logic
    
    if add_voice and script:
        with st.spinner("Step 3: Synthesizing Voice..."):
            audio_path = asyncio.run(generator.generate_voice(script, VOICES[voice_choice]))
        
        final_video = generator.assemble_final_reel(motion_path, audio_path, video_len)
        st.video(final_video)
