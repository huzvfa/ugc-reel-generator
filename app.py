import streamlit as st
import asyncio
import os
import subprocess
from core import generator

st.set_page_config(page_title="HOVER AI | THE BREAKTHROUGH", layout="wide", initial_sidebar_state="expanded")

# --- ELITE GLOSSY CSS ---
st.markdown("""
    <style>
    .stApp { background: #020202; color: #ffffff; }
    .glass-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(0, 242, 254, 0.2);
        border-radius: 15px; padding: 25px;
        box-shadow: 0 0 30px rgba(0, 242, 254, 0.05);
    }
    .hover-glow { color: #00f2fe; text-shadow: 0 0 10px #00f2fe; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- HOVER AI SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 class='hover-glow'>💠 HOVER AI</h1>", unsafe_allow_html=True)
    st.caption("Engine Version: 1.0.4-Breakthrough")
    app_mode = st.selectbox("Switch Interface", ["Neural Chat", "UGC Studio", "Vision Lab"])
    st.divider()
    st.markdown("### System Status")
    st.success("Core: Online")
    st.success("Vision: Active")
    st.success("Neural: Ready")

# --- MODULE 1: NEURAL CHAT (Hover AI Identity) ---
if app_mode == "Neural Chat":
    st.markdown("<h2 class='hover-glow'>Neural Communication Link</h2>", unsafe_allow_html=True)
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    if user_query := st.chat_input("Speak to Hover AI..."):
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"): st.markdown(user_query)

        with st.chat_message("assistant"):
            # Real-time responsiveness simulation
            thinking_placeholder = st.empty()
            thinking_placeholder.markdown("*Hover AI is thinking...*")
            response = generator.hover_chat(user_query)
            thinking_placeholder.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

# --- MODULE 2: UGC STUDIO (Video & Sync) ---
elif app_mode == "UGC Studio":
    st.markdown("<h2 class='hover-glow'>UGC Video Production</h2>", unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        tool = st.selectbox("Toolchain:", ["Text-to-Video", "Image-to-Video", "Image-to-Image"])
        prompt = st.text_area("Describe Scenario & Motion:", height=100)
        
        use_voice = st.toggle("Enable Neural Voiceover", value=True)
        if use_voice:
            script = st.text_area("Enter Script:")
            timer = st.slider("Target Duration (s):", 5, 30, 10)
            voices = {"USA (F)": "en-US-AnaNeural", "UK (M)": "en-GB-RyanNeural", "Urdu (F)": "ur-PK-UzmaNeural"}
            v_choice = st.selectbox("Neural Voice Agent:", list(voices.keys()))

    with col2:
        u_file = st.file_uploader("Reference Visual", type=['png','jpg']) if "Image" in tool else None
        
        if st.button("🚀 INITIATE HOVER ENGINE", use_container_width=True):
            with st.spinner("Synthesizing Multimodal Content..."):
                # 1. Base Image
                img_path = generator.query_image_gen(prompt)
                
                # 2. Motion Generation
                ref = img_path if tool != "Image-to-Video" else u_file
                motion_path = generator.query_video_motion(prompt, image_path=ref)
                
                if motion_path:
                    if use_voice and script:
                        audio_path = asyncio.run(generator.generate_voice(script, voices[v_choice], "output/audio.mp3"))
                        final_reel = generator.sync_audio_video(motion_path, audio_path, timer)
                        st.video(final_reel)
                    else:
                        st.video(motion_path)
    st.markdown('</div>', unsafe_allow_html=True)
