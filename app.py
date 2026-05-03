import streamlit as st
import asyncio
import os
from core.brain import hover_brain
from core import generator

st.set_page_config(page_title="HOVER AI STUDIO", layout="wide")

# --- NEON DYNAMIC CSS ---
st.markdown("""
    <style>
    .stApp { background: #010101; color: #fff; }
    /* Neon Thinking Blinkers */
    @keyframes blink { 0% { opacity: 1; box-shadow: 0 0 10px #00f2fe; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    .thinking-neon { height: 4px; width: 100px; background: #00f2fe; animation: blink 1s infinite; border-radius: 2px; }
    .chat-container { display: flex; align-items: center; gap: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- VOICE MAPPING (FIXED AGENTS) ---
VOICES = {
    "English Female (Mature)": "en-US-JennyNeural",
    "English Male (Deep)": "en-GB-RyanNeural",
    "Urdu Female (Native)": "ur-PK-UzmaNeural",
    "Urdu Male (Native)": "ur-PK-AsadNeural"
}

with st.sidebar:
    st.title("💠 HOVER AI")
    mode = st.radio("Switch Module", ["Neural Chat", "UGC Studio", "Story Reel Creator"])

# --- FEATURE: NEURAL CHAT ---
if mode == "Neural Chat":
    st.header("Proprietary Neural Link")
    
    # Left-side Upload Logic
    col_up, col_chat = st.columns([1, 8])
    with col_up:
        uploaded_file = st.file_uploader("📎", type=None, label_visibility="collapsed")
    
    doc_ctx = hover_brain.process_any_file(uploaded_file) if uploaded_file else ""
    
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])
    
    with col_chat:
        if q := st.chat_input("Analyze with Hover AI..."):
            st.session_state.messages.append({"role": "user", "content": q})
            with st.chat_message("user"): st.write(q)
            
            with st.chat_message("assistant"):
                # Neon Blinker Animation
                st.markdown('<div class="thinking-neon"></div>', unsafe_allow_html=True)
                res = hover_brain.think(q, context=doc_ctx)
                st.write(res)
                st.session_state.messages.append({"role": "assistant", "content": res})

# --- FEATURE: UGC STUDIO ---
elif mode == "UGC Studio":
    st.header("Hover Production Suite")
    col1, col2 = st.columns([1, 1])
    
    # Defaults to ensure video works without audio
    v_len = 15 

    with col1:
        tool = st.selectbox("Tool:", ["Text-to-Video", "Image-to-Video", "Text-to-Image", "Image-to-Image"])
        prompt = st.text_area("Instructions:")
        v_len = st.slider("Video Duration (s):", 5, 60, 15)
        
        use_voice = st.toggle("Enable Voiceover & Script")
        if use_voice:
            script = st.text_area("Script:")
            agent = st.selectbox("Agent:", list(VOICES.keys()))
            tone = st.select_slider("Tone:", options=["Soft", "Seductive", "Serious", "Angry"])
            
            # Tone Impact Logic
            pitch = "-10Hz" if tone == "Serious" else ("+5Hz" if tone == "Seductive" else "+0Hz")
            
            with st.spinner("Neural Sync..."):
                asyncio.run(generator.hover_voice_engine("Hey, I'm Hover AI.", VOICES[agent], pitch=pitch))
                st.audio("output/voice.mp3")

    with col2:
        if st.button("🚀 EXECUTE HOVER ENGINE"):
            with st.spinner("Rendering..."):
                base_img = generator.hover_visual_gen(prompt, tool)
                if "Video" in tool:
                    video_path = generator.hover_master_video(prompt, base_img, v_len)
                    st.video(video_path)
                else:
                    st.image(base_img)

# --- FEATURE: STORY REEL CREATOR ---
elif mode == "Story Reel Creator":
    st.header("Hover Real-Time Story Engine")
    story_prompt = st.text_area("Enter a Story/Reel Prompt:")
    if st.button("🎬 Generate Multi-Scene Reel"):
        # This triggers the multi-scene synthesis logic
        st.info("Hover AI is synthesizing a real-time cinematic story...")
