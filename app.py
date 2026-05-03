import streamlit as st
import asyncio
import os
from core import generator

st.set_page_config(page_title="Hover AI | Multimodal Studio", layout="wide")

# --- GLOSSY MODERN UI ---
st.markdown("""
    <style>
    .stApp { background: #050505; color: #fff; }
    .glass { background: rgba(255,255,255,0.03); border-radius: 15px; border: 1px solid #333; padding: 25px; }
    .sidebar-btn { width: 100%; border-radius: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("💠 HOVER AI")
    app_mode = st.radio("Switch Feature", ["Elite Chat", "UGC Video Studio", "Asset Generator"])

# --- FEATURE 1: ELITE CHAT (Gemini/Claude Rival) ---
if app_mode == "Elite Chat":
    st.header("Hover AI Assistant")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if chat_input := st.chat_input("Ask Hover AI anything..."):
        st.session_state.messages.append({"role": "user", "content": chat_input})
        with st.chat_message("user"):
            st.markdown(chat_input)

        with st.chat_message("assistant"):
            response = generator.hover_chat(chat_input)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- FEATURE 2: VIDEO STUDIO (True Motion) ---
elif app_mode == "UGC Video Studio":
    st.header("Hover AI Video Engine")
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        mode = st.selectbox("Tool:", ["Text-to-Video", "Image-to-Video", "Image-to-Image"])
        prompt = st.text_area("Describe the ACTION (e.g. 'Person running on a road, camera follows'):")
        
        # Restoration of the Video Timer & Script toggle
        use_script = st.toggle("Enable Script & Voiceover", value=True)
        if use_script:
            script = st.text_area("Enter Script:")
            video_duration = st.slider("Duration (Seconds):", 5, 30, 10)
            
            voices = {"USA Female": "en-US-AnaNeural", "UK Male": "en-GB-RyanNeural", "Urdu Male": "ur-PK-AsadNeural"}
            v_choice = st.selectbox("Voice Agent:", list(voices.keys()))
            
        uploaded_file = st.file_uploader("Upload reference photo", type=['jpg','png']) if "Image-" in mode else None
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if st.button("🚀 INITIATE GENERATION"):
            with st.spinner("Hover AI is rendering motion..."):
                # 1. Base Image (if needed)
                img_path = generator.query_image_gen(prompt) if mode == "Text-to-Video" else None
                
                # 2. ACTUAL AI MOTION
                motion_path = generator.query_video_motion(prompt, image_path=img_path if img_path else (uploaded_file if uploaded_file else None))
                
                # 3. VOICE & SYNC
                if motion_path:
                    if use_script and script:
                        audio_path = asyncio.run(generator.generate_voice(script, voices[v_choice], "output/audio.mp3"))
                        final_reel = generator.sync_audio_video(motion_path, audio_path, video_duration)
                        st.video(final_reel)
                    else:
                        st.video(motion_path)
                else:
                    st.error("Engine Busy. High-quality motion takes 30-60s on free tier.")
