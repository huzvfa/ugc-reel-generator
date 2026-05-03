import streamlit as st
import asyncio
from core import generator

st.title("🚀 Pro UGC AI Content Suite")

# --- 1. UPLOAD ---
uploaded_file = st.file_uploader("Choose a JPG/PNG...", type=["jpg", "png"])

# --- 2. CONFIGURE ---
st.header("2. Configure Generator")
col1, col2 = st.columns(2)

with col1:
    prompt = st.text_area("Describe your AI Scenario:", placeholder="A traveler sipping coffee in Northern Pakistan...")
    script = st.text_area("Script:", "Check out this view! Use my code for 10% off.")
    
    # NEW: Voice Selection
    voices = {
        "Male (Professional)": "en-US-ChristopherNeural",
        "Female (Energetic)": "en-US-AnaNeural",
        "Male (Casual)": "en-GB-RyanNeural",
        "Female (Soft)": "en-US-MichelleNeural"
    }
    selected_voice = st.selectbox("Select Voiceover Agent:", list(voices.keys()))

with col2:
    mode = st.radio("Generation Mode:", 
                    ["Text-to-Image", "Image-to-Image", "Text-to-Video", "Image-to-Video"])
    
    # NEW: Duration Timer
    video_duration = st.slider("Target Video Length (Seconds):", 5, 30, 15)

# --- 3. GENERATE ---
if st.button("Generate AI Content"):
    # Path logic
    img_path = None
    
    # Step A: Image Generation (Base for Video or standalone)
    with st.spinner("Generating Visuals..."):
        if "Image" in mode and uploaded_file:
            img_path = generator.query_im2im_gen(uploaded_file, prompt)
        else:
            img_path = generator.query_image_gen(prompt)
        st.image(img_path, width=300)

    # Step B: Voiceover
    with st.spinner("Synthesizing Voice..."):
        audio_path = asyncio.run(generator.generate_voice(script, voices[selected_voice]))
        st.audio(audio_path)

    # Step C: Video (If selected)
    if "Video" in mode:
        with st.spinner(f"Rendering {video_duration}s Video..."):
            video_path = generator.query_video_gen(img_path, video_duration)
            if video_path:
                st.video(video_path)

    st.success("Assets ready for GitHub Repo!")
