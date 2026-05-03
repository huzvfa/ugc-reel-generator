import streamlit as st
import asyncio
from core import generator
import os

# --- MODERN UI STYLING (Neon Glow & Borders) ---
st.set_page_config(page_title="UGC AI Suite", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #00f2fe 0%, #4facfe 100%);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.4);
    }
    .stTextArea textarea, .stTextInput input {
        border: 1px solid #4facfe !important;
        background-color: #1a1c24 !important;
        color: white !important;
    }
    .neon-border {
        border: 1px solid #4facfe;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(79, 172, 254, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 UGC AI Reel Generator")
st.markdown("---")

# --- 1. UPLOAD SECTION ---
with st.container():
    st.markdown('<div class="neon-border">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a reference JPG/PNG...", type=["jpg", "png", "jpeg"])
    st.markdown('</div>', unsafe_allow_html=True)

st.write("") # Spacer

# --- 2. CONFIGURE SECTION ---
st.header("2. Configure Generator")

col1, col2 = st.columns([1.5, 1])

with col2:
    mode = st.radio(
        "Generation Mode:", 
        ["Text-to-Image", "Image-to-Image", "Text-to-Video", "Image-to-Video"],
        index=0
    )

with col1:
    prompt = st.text_area("Describe your AI Scenario:", placeholder="A person wearing a hoodie walking through Islamabad...")
    
    # CONDITION 1: Show Script and Timer ONLY for Video modes
    if "Video" in mode:
        st.markdown("---")
        script = st.text_area("Video Script:", "Check out this amazing vibe! #UGC")
        video_duration = st.slider("Target Video Length (Seconds):", 5, 30, 15)
        
        # VOICE AGENT SELECTION
        voices = {
            "Male (Professional)": "en-US-ChristopherNeural",
            "Female (Energetic)": "en-US-AnaNeural",
            "Male (Casual)": "en-GB-RyanNeural",
            "Female (Soft)": "en-US-MichelleNeural"
        }
        selected_voice_label = st.selectbox("Select Voiceover Agent:", list(voices.keys()))
        selected_voice_code = voices[selected_voice_label]

        # NEW: Voice Preview Feature
        if st.button("🔊 Preview Voice"):
            preview_path = "voice_preview.mp3"
            asyncio.run(generator.generate_voice("This is a preview of your selected AI voice agent.", selected_voice_code, preview_path))
            st.audio(preview_path)

# --- 3. EXECUTION ---
st.markdown("---")
if st.button("🚀 Generate Final UGC Content"):
    if ("Image-to" in mode or "Image-Video" in mode) and uploaded_file is None:
        st.error("Please upload an image first for this mode!")
    else:
        # Create output dir if not exists
        if not os.path.exists("output"):
            os.makedirs("output")

        with st.spinner("Processing AI Pipeline..."):
            # A. Visual Generation
            if "Image-to" in mode and uploaded_file:
                img_path = generator.query_im2im_gen(uploaded_file, prompt)
            else:
                img_path = generator.query_image_gen(prompt)
            
            st.image(img_path, caption="Generated Visual Base", width=400)

            # B. Audio & Video logic for Video Modes
            if "Video" in mode:
                audio_path = asyncio.run(generator.generate_voice(script, selected_voice_code, "output/final_voice.mp3"))
                video_clip_path = generator.query_video_gen(img_path, video_duration)
                
                if video_clip_path:
                    st.success("Reel Generated successfully!")
                    st.video(video_clip_path)
                    st.audio(audio_path)
