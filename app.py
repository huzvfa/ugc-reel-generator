import streamlit as st
import asyncio
import os
import subprocess
from core import generator

st.set_page_config(page_title="HOVER AI | THE BREAKTHROUGH", layout="wide")

# --- GLOBAL SCOPE DEFINITIONS (Fixes NameError) ---
VOICE_AGENTS = {
    "USA (Female)": "en-US-AnaNeural",
    "UK (Male)": "en-GB-RyanNeural",
    "Urdu (Female)": "ur-PK-UzmaNeural",
    "Urdu (Male)": "ur-PK-AsadNeural"
}

# --- GLOSSY DASHBOARD UI ---
st.markdown("""
    <style>
    .stApp { background: #010101; color: #ffffff; }
    .glass-panel {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(0, 242, 254, 0.3);
        border-radius: 20px; padding: 25px;
        box-shadow: 0 0 30px rgba(0, 242, 254, 0.1);
    }
    .hover-brand { color: #00f2fe; text-shadow: 0 0 10px #00f2fe; font-size: 2rem; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<div class='hover-brand'>HOVER AI</div>", unsafe_allow_html=True)
    mode = st.selectbox("Switch Module", ["Neural Chat", "UGC Studio", "Vision Lab"])
    st.divider()
    st.info("Status: Breakthrough Engine Active")

# --- MODULE 1: PROPRIETARY CHAT ---
if mode == "Neural Chat":
    st.header("Proprietary Neural Link")
    if "messages" not in st.session_state: st.session_state.messages = []
    
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])

    if query := st.chat_input("Speak to HOVER AI..."):
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"): st.write(query)
        
        with st.chat_message("assistant"):
            response = generator.hover_neural_chat(query)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- MODULE 2: VIDEO STUDIO (The Fix) ---
elif mode == "UGC Studio":
    st.header("Hover Mastering Engine")
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        tool = st.selectbox("Tool:", ["Text-to-Video", "Image-to-Video", "Text-to-Image"])
        prompt = st.text_area("Instructions:")
        script = st.text_area("Voiceover Script (Optional):")
        duration = st.slider("Duration (s):", 5, 30, 10)
        agent = st.selectbox("Voice:", list(VOICE_AGENTS.keys()))

    with col2:
        u_file = st.file_uploader("Reference", type=['png','jpg']) if "Image-" in tool else None
        if st.button("🚀 INITIATE ENGINE", use_container_width=True):
            with st.spinner("Processing..."):
                img_path = generator.hover_vision_gen(prompt)
                
                if tool == "Text-to-Image":
                    st.image(img_path)
                else:
                    # Video Logic with Fix for NameError
                    ref = img_path if "Text-" in tool else u_file
                    motion = generator.hover_motion_engine(prompt, image_path=ref)
                    
                    # Fallback for busy API
                    if motion == "reflex_motion":
                        audio_p = asyncio.run(generator.hover_voice_gen("..", VOICE_AGENTS[agent], "output/s.mp3"))
                        motion = generator.hover_sync_engine(img_path, audio_p, 5)

                    if script:
                        audio = asyncio.run(generator.hover_voice_gen(script, VOICE_AGENTS[agent], "output/a.mp3"))
                        final = generator.hover_sync_engine(motion, audio, duration)
                        st.video(final)
                    else:
                        st.video(motion)
    st.markdown('</div>', unsafe_allow_html=True)
