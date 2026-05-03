import streamlit as st
import asyncio
import os
from core.agent import hover_agent
from core import generator

st.set_page_config(page_title="HOVER AI STUDIO", layout="wide")

# --- CYBERPUNK CHAT CSS ---
st.markdown("""
    <style>
    .stApp { background: #010101; color: #fff; }
    /* Neon Thinking Pulse */
    @keyframes pulse { 0% { box-shadow: 0 0 2px #00f2fe; } 50% { box-shadow: 0 0 15px #00f2fe; } 100% { box-shadow: 0 0 2px #00f2fe; } }
    .thinking-neon { height: 2px; width: 100%; background: #00f2fe; animation: pulse 1s infinite; margin: 10px 0; }
    /* Input Container Styling */
    .stChatInputContainer { padding-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

VOICES = {
    "Male (Deep)": "en-GB-RyanNeural",
    "Female (Mature)": "en-US-JennyNeural",
    "Female (Urdu)": "ur-PK-UzmaNeural",
    "Male (Urdu)": "ur-PK-AsadNeural"
}

with st.sidebar:
    st.markdown("<h1 style='color:#00f2fe;'>💠 HOVER AI</h1>", unsafe_allow_html=True)
    mode = st.radio("Neural Interface", ["Neural Chat", "UGC Studio"])

# --- MODULE 1: NEURAL CHAT (Redesigned Input) ---
if mode == "Neural Chat":
    st.header("Proprietary Neural Link")
    
    # Message Display
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])

    # REDESIGNED INPUT AREA: Upload and Text in one line
    st.divider()
    input_col, file_col = st.columns([0.08, 0.92])
    
    with input_col:
        # Small icon-only uploader next to the text box
        doc = st.file_uploader("📎", type=None, label_visibility="collapsed")
    
    with file_col:
        q = st.chat_input("Analyze or ask HOVER AI...")

    if q:
        context = hover_agent.analyze_deep(doc) if doc else ""
        st.session_state.messages.append({"role": "user", "content": q})
        with st.chat_message("user"): st.write(q)
        
        with st.chat_message("assistant"):
            st.markdown('<div class="thinking-neon"></div>', unsafe_allow_html=True)
            res = hover_agent.solve(q, context=context)
            st.write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

# --- MODULE 2: UGC STUDIO ---
elif mode == "UGC Studio":
    st.header("Hover Production Suite")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        tool = st.selectbox("Tool:", ["Text-to-Video", "Image-to-Video", "Text-to-Image", "Image-to-Image"])
        prompt = st.text_area("Hover Instructions:")
        timer = st.slider("Length (s):", 5, 60, 15)
        
        use_voice = st.toggle("Enable Voiceover")
        if use_voice:
            script = st.text_area("Script:")
            agent = st.selectbox("Agent:", list(VOICES.keys()))
            tone = st.select_slider("Tone:", options=["Soft", "Seductive", "Serious", "Angry"])
            
            with st.spinner(""):
                asyncio.run(generator.hover_voice_engine("Hey, I'm Hover AI.", VOICES[agent], tone))
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
