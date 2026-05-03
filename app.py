import streamlit as st
import asyncio
import os
from core.agent import hover_agent
from core import generator

st.set_page_config(page_title="HOVER AI STUDIO", layout="wide")

# --- GLOBAL STYLES ---
st.markdown("<style>.stApp { background: #010101; color: #fff; }</style>", unsafe_allow_html=True)
VOICES = {"Male (Deep)": "en-GB-RyanNeural", "Female (Mature)": "en-US-JennyNeural", "Urdu Female": "ur-PK-UzmaNeural", "Urdu Male": "ur-PK-AsadNeural"}

with st.sidebar:
    st.markdown("<h1 style='color:#00f2fe;'>💠 HOVER AI</h1>", unsafe_allow_html=True)
    mode = st.radio("Neural Interface", ["Neural Chat", "UGC Studio", "Story Reel Creator"])

# --- MODULE: NEURAL CHAT ---
if mode == "Neural Chat":
    st.header("Proprietary Neural Link")
    if "messages" not in st.session_state: st.session_state.messages = []
    
    # Unified Command Bar
    st.divider()
    btn_col, input_col = st.columns([0.1, 0.9])
    with btn_col:
        doc = st.file_uploader("📎", type=None, label_visibility="collapsed")
    with input_col:
        query = st.chat_input("Command HOVER AI...")

    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"): st.write(query)
        with st.chat_message("assistant"):
            st.markdown('<div style="height:2px;width:100%;background:#00f2fe;box-shadow:0 0 10px #00f2fe;"></div>', unsafe_allow_html=True)
            context = hover_agent.analyze_deep(doc) if doc else ""
            res = hover_agent.solve(query, context=context)
            st.write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

# --- MODULE: UGC STUDIO ---
elif mode == "UGC Studio":
    st.header("Hover Production Suite")
    
    # NSFW Detection Logic
    is_nsfw = any(x in st.session_state.get('p_check', '').lower() for x in ['nsfw', '18+', 'adult'])
    if is_nsfw and not st.session_state.get('verified'):
        st.warning("⚠️ 18+ Content Detected. Proceed?")
        if st.button("Confirm 18+"):
            st.session_state.verified = True
            st.rerun()
        st.stop()

    col1, col2 = st.columns([1, 1])
    with col1:
        tool = st.selectbox("Tool Mode:", ["Text-to-Video", "Image-to-Video", "Text-to-Image", "Image-to-Image"])
        prompt = st.text_area("Instructions:")
        st.session_state.p_check = prompt
        timer = st.slider("Duration (s):", 5, 60, 15)
        
        use_voice = st.toggle("Enable Voiceover")
        if use_voice:
            script = st.text_area("Script:")
            agent = st.selectbox("Agent:", list(VOICES.keys()))
            tone = st.select_slider("Tone:", options=["Soft", "Seductive", "Serious"])
            asyncio.run(generator.hover_voice_engine("Neural Tone Synced.", VOICES[agent], tone))
            st.audio("output/voice.mp3")

    with col2:
        u1 = st.file_uploader("Upload Image", type=['png','jpg']) if "Image-" in tool else None
        if st.button("🚀 EXECUTE ENGINE"):
            with st.spinner("Rendering..."):
                base = generator.hover_visual_gen(prompt, tool, u1)
                if "Video" in tool:
                    video = generator.hover_video_gen(prompt, base, timer)
                    st.video(video)
                else:
                    st.image(base)
