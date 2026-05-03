import streamlit as st
import asyncio
import os
from core.agent import hover_agent
from core import generator

st.set_page_config(page_title="HOVER AI STUDIO", layout="wide")

# --- NEON GLOW UI ---
st.markdown("""
    <style>
    .stApp { background: #010101; color: #fff; }
    @keyframes pulse { 0% { box-shadow: 0 0 5px #00f2fe; } 50% { box-shadow: 0 0 20px #00f2fe; } 100% { box-shadow: 0 0 5px #00f2fe; } }
    .thinking-neon { height: 2px; width: 100%; background: #00f2fe; animation: pulse 1.5s infinite; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

VOICES = {"Male (English)": "en-GB-RyanNeural", "Female (English)": "en-US-JennyNeural", "Female (Urdu)": "ur-PK-UzmaNeural", "Male (Urdu)": "ur-PK-AsadNeural"}

with st.sidebar:
    st.markdown("<h1 style='color:#00f2fe;'>💠 HOVER AI</h1>", unsafe_allow_html=True)
    mode = st.radio("Neural Interface", ["Neural Chat", "UGC Studio", "Story Reel Creator"])

# --- NEURAL CHAT (INTEGRATED UPLOAD) ---
if mode == "Neural Chat":
    st.header("Proprietary Neural Link")
    col_up, col_chat = st.columns([0.1, 0.9])
    with col_up:
        doc = st.file_uploader("📎", type=None, label_visibility="collapsed")
    with col_chat:
        query = st.chat_input("Command HOVER AI...")

    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])

    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"): st.write(query)
        with st.chat_message("assistant"):
            st.markdown('<div class="thinking-neon"></div>', unsafe_allow_html=True)
            context = hover_agent.analyze_deep(doc) if doc else ""
            res = hover_agent.solve(query, context=context)
            st.write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

# --- UGC STUDIO (NSFW GUARD + MULTI-MODE) ---
elif mode == "UGC Studio":
    st.header("Hover Production Suite")
    
    # NSFW Intent Detection Agent
    is_nsfw = any(x in st.session_state.get('p_check', '').lower() for x in ['nsfw', '18+', 'adult', 'naked'])
    if is_nsfw and not st.session_state.get('verified'):
        st.warning("⚠️ NSFW Intent Detected. Are you over 18?")
        if st.button("Confirm 18+"):
            st.session_state.verified = True
            st.rerun()
        st.stop()

    col1, col2 = st.columns([1, 1])
    with col1:
        tool = st.selectbox("Tool Mode:", ["Text-to-Video", "Image-to-Video", "Text-to-Image", "Image-to-Image"])
        prompt = st.text_area("Hover Instructions:")
        st.session_state.p_check = prompt
        timer = st.slider("Length (s):", 5, 60, 15)
        
        use_voice = st.toggle("Enable Voiceover")
        if use_voice:
            script = st.text_area("Script:")
            agent = st.selectbox("Agent:", list(VOICES.keys()))
            tone = st.select_slider("Tone:", options=["Soft", "Seductive", "Serious", "Angry"])
            asyncio.run(generator.hover_voice_engine("Previewing Neural Tone...", VOICES[agent], tone))
            st.audio("output/voice.mp3")

    with col2:
        u1 = st.file_uploader("Upload Image Reference", type=['png','jpg']) if "Image-" in tool else None
        if st.button("🚀 EXECUTE ENGINE"):
            with st.spinner("Processing Multi-Agent Synergy..."):
                base = generator.hover_visual_gen(prompt, tool, u1)
                if "Video" in tool:
                    video = generator.hover_video_gen(prompt, base, timer)
                    st.video(video)
                else:
                    st.image(base)

# --- STORY REEL CREATOR ---
elif mode == "Story Reel Creator":
    st.header("Proprietary Story Sequencer")
    s_prompt = st.text_area("Describe the cinematic story:")
    if st.button("🎬 GENERATE REEL"):
        with st.spinner("Compiling Neural Scenes..."):
            scene = generator.hover_visual_gen(s_prompt, "Text-to-Video")
            final = generator.hover_video_gen(s_prompt, scene, 30)
            if final: st.video(final)
