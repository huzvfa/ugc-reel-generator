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
    @keyframes neural-glow { 0% { opacity: 0.5; } 50% { opacity: 1; box-shadow: 0 0 15px #00f2fe; } 100% { opacity: 0.5; } }
    .thinking-line { height: 2px; width: 100%; background: #00f2fe; animation: neural-glow 1.5s infinite; margin: 10px 0; }
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
    mode = st.radio("Neural Interface", ["Neural Chat", "UGC Studio", "Story Reel Creator"])

# --- MODULE 1: NEURAL CHAT ---
if mode == "Neural Chat":
    st.header("Proprietary Neural Link")
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])

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
            st.markdown('<div class="thinking-line"></div>', unsafe_allow_html=True)
            context = hover_agent.analyze_deep(doc) if doc else ""
            res = hover_agent.solve(query, context=context)
            st.write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

# --- MODULE 2: UGC STUDIO (RESTORED) ---
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

# --- MODULE 3: STORY REEL CREATOR ---
elif mode == "Story Reel Creator":
    st.header("Proprietary Story Sequencer")
    story_prompt = st.text_area("Describe the cinematic story:")
    if st.button("🎬 GENERATE FULL STORY"):
        with st.spinner("Synthesizing..."):
            scene = generator.hover_visual_gen(story_prompt, "Text-to-Video")
            final_story = generator.hover_video_gen(story_prompt, scene, 30)
            if final_story:
                st.video(final_story)
