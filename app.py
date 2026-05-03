import streamlit as st
import asyncio
import os
import subprocess
from core import generator

st.set_page_config(page_title="HOVER AI | THE BREAKTHROUGH", layout="wide")

# --- GLOSSY GLASS UI ---
st.markdown("""
    <style>
    .stApp { background: #010101; color: #ffffff; font-family: 'Inter', sans-serif; }
    .glass-panel {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(0, 242, 254, 0.3);
        border-radius: 20px; padding: 25px;
        box-shadow: 0 0 40px rgba(0, 242, 254, 0.1);
    }
    .hover-brand { color: #00f2fe; text-shadow: 0 0 15px #00f2fe; font-size: 2.5rem; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

# --- HOVER AI CONTROL PANEL ---
with st.sidebar:
    st.markdown("<div class='hover-brand'>HOVER AI</div>", unsafe_allow_html=True)
    st.caption("v1.0.5 Breakthrough Edition")
    mode = st.selectbox("Switch Neural Module", ["Neural Chat", "UGC Video Studio", "Vision Lab"])
    st.divider()
    st.info("Status: Optimized & Proprietary")

# --- MODULE: NEURAL CHAT ---
if mode == "Neural Chat":
    st.header("Proprietary Neural Link")
    if "messages" not in st.session_state: st.session_state.messages = []
    
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])

    if query := st.chat_input("Input command for Hover AI..."):
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"): st.write(query)
        
        with st.chat_message("assistant"):
            thinking = st.empty()
            thinking.markdown("Thinking...")
            response = generator.hover_neural_chat(query)
            thinking.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- MODULE: UGC VIDEO STUDIO ---
elif mode == "UGC Video Studio":
    st.header("Hover AI Video Mastering")
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        tool = st.selectbox("Select Tool:", ["Text-to-Video", "Image-to-Video", "Image-to-Image", "Text-to-Image"])
        prompt = st.text_area("Hover Engine Instructions:", placeholder="Describe the scene and the movement...")
        
        use_voice = st.toggle("Enable Neural Voice", value=True)
        if use_voice:
            script = st.text_area("Voiceover Script:")
            timer = st.slider("Video Timer (s):", 5, 30, 10)
            voice_agent = st.selectbox("Agent:", ["USA Female", "UK Male", "Urdu Female"])
            v_map = {"USA Female": "en-US-AnaNeural", "UK Male": "en-GB-RyanNeural", "Urdu Female": "ur-PK-UzmaNeural"}

    with col2:
        u_file = st.file_uploader("Reference Media", type=['png','jpg']) if "Image-" in tool else None
        
        if st.button("🚀 EXECUTE HOVER ENGINE", use_container_width=True):
            with st.spinner("Processing..."):
                # Logic Flow
                if tool == "Text-to-Image":
                    res_path = generator.hover_vision_gen(prompt)
                    st.image(res_path)
                else:
                    # Video/Motion Logic
                    img_base = generator.hover_vision_gen(prompt) if "Text-" in tool else None
                    ref_path = img_base if img_base else (u_file if u_file else None)
                    
                    motion_path = generator.hover_motion_engine(prompt, image_path=ref_path)
                    
                    if motion_path == "reflex_motion":
                        st.warning("Deep Motion Busy: Utilizing Hover Reflex Engine...")
                        # FFmpeg creates a cinematic motion reel from the vision base
                        motion_path = generator.hover_sync_engine(img_base, asyncio.run(generator.hover_voice_gen("..", v_map[voice_agent], "output/s.mp3")), 5)

                    if use_voice and script:
                        audio = asyncio.run(generator.hover_voice_gen(script, v_map[voice_agent], "output/a.mp3"))
                        final = generator.hover_sync_engine(motion_path, audio, timer)
                        st.video(final)
                    else:
                        st.video(motion_path)
    st.markdown('</div>', unsafe_allow_html=True)
