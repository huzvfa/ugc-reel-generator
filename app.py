import streamlit as st
import asyncio
import os
from core import generator

st.set_page_config(page_title="Hover AI | Breakthrough Studio", layout="wide")

# --- GLOSSY NEON UI ---
st.markdown("""
    <style>
    .stApp { background: #050505; color: #fff; }
    .glass { 
        background: rgba(255,255,255,0.02); 
        border: 1px solid rgba(255,255,255,0.1); 
        border-radius: 15px; padding: 25px; 
    }
    .stButton>button {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        border: none; color: white; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px #00f2fe; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("💠 HOVER AI")
    app_mode = st.radio("Switch Module", ["Elite Chat", "UGC Video Studio", "Asset Generator"])
    st.divider()
    st.info("Operating at Breakthrough Speed")

# --- FEATURE 1: ELITE CHAT (Llama-3 70B Engine) ---
if app_mode == "Elite Chat":
    st.header("Hover AI Assistant")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if chat_input := st.chat_input("Message Hover AI..."):
        st.session_state.messages.append({"role": "user", "content": chat_input})
        with st.chat_message("user"): st.markdown(chat_input)

        with st.chat_message("assistant"):
            # Fixed call to choices[0] logic in generator
            response = generator.hover_chat(chat_input)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- FEATURE 2: VIDEO STUDIO (True Motion Sync) ---
elif app_mode == "UGC Video Studio":
    st.header("Hover AI Video Engine")
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        tool = st.selectbox("Tool:", ["Text-to-Video", "Image-to-Video", "Image-to-Image"])
        prompt = st.text_area("Describe Action/Scenario:", placeholder="Person walking through a rainy neon city...")
        
        # USER OPTIONS
        use_voice = st.toggle("Enable Voiceover & Script", value=True)
        if use_voice:
            script = st.text_area("Script:")
            video_timer = st.slider("Target Duration (s):", 5, 30, 10)
            voices = {"USA Female": "en-US-AnaNeural", "UK Male": "en-GB-RyanNeural", "PK Urdu": "ur-PK-UzmaNeural"}
            v_choice = st.selectbox("Voice Agent:", list(voices.keys()))
            
        u_file = st.file_uploader("Upload reference", type=['jpg','png']) if "Image-" in tool else None
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if st.button("🚀 INITIATE HOVER ENGINE", use_container_width=True):
            with st.spinner("Rendering actual AI motion..."):
                # 1. Image Base
                img_path = generator.query_image_gen(prompt) if tool == "Text-to-Video" else None
                
                # 2. Real Motion Clip
                ref_path = img_path if img_path else (u_file if u_file else None)
                motion_path = generator.query_video_motion(prompt, image_path=ref_path)
                
                if motion_path:
                    if use_voice and script:
                        audio_path = asyncio.run(generator.generate_voice(script, voices[v_choice], "output/audio.mp3"))
                        final_reel = generator.sync_audio_video(motion_path, audio_path, video_timer)
                        st.video(final_reel)
                    else:
                        st.video(motion_path)
                else:
                    st.error("Engine Timeout. Try again in 30s.")
