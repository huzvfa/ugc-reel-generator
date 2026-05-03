import streamlit as st
import asyncio
import os
from core.agent import hover_agent
from core import generator

st.set_page_config(page_title="HOVER AI STUDIO", layout="wide")

# --- CSS: NEON BLINKERS & DYNAMIC CHAT ---
st.markdown("""
    <style>
    .stApp { background: #010101; color: #fff; }
    @keyframes pulse { 0% { box-shadow: 0 0 5px #00f2fe; } 50% { box-shadow: 0 0 20px #00f2fe; } 100% { box-shadow: 0 0 5px #00f2fe; } }
    .thinking-neon { height: 2px; width: 100%; background: #00f2fe; animation: pulse 1.5s infinite; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

VOICES = {
    "Male (Deep English)": "en-GB-RyanNeural",
    "Female (Mature English)": "en-US-JennyNeural",
    "Female (Soft Urdu)": "ur-PK-UzmaNeural",
    "Male (Professional Urdu)": "ur-PK-AsadNeural"
}

with st.sidebar:
    st.markdown("<h1 style='color:#00f2fe;'>💠 HOVER AI</h1>", unsafe_allow_html=True)
    mode = st.radio("Neural Interface", ["Neural Chat", "UGC Studio", "Story Reel Creator"])

# --- MODULE 1: NEURAL CHAT ---
if mode == "Neural Chat":
    st.header("Proprietary Neural Link")
    col_up, col_chat = st.columns([1, 8])
    with col_up:
        doc = st.file_uploader("📎", type=None, label_visibility="collapsed")
    
    context = hover_agent.analyze_deep(doc) if doc else ""
    
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])
    
    if q := st.chat_input("Speak to HOVER AI..."):
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
        timer = st.slider("Video Length (s):", 5, 60, 15)
        
        use_voice = st.toggle("Enable Voiceover")
        if use_voice:
            script = st.text_area("Script:")
            agent = st.selectbox("Agent:", list(VOICES.keys()))
            tone = st.select_slider("Tone:", options=["Soft", "Charming", "Seductive", "Serious", "Angry"])
            asyncio.run(generator.hover_voice_engine("Hey, I'm Hover AI, your proprietary engine.", VOICES[agent], tone))
            st.audio("output/voice.mp3")

    with col2:
        u1 = st.file_uploader("Reference Image", type=['png','jpg']) if "Image-" in tool else None
        if st.button("🚀 EXECUTE ENGINE"):
            with st.spinner("Processing..."):
                # FIXED: Corrected function call to visual_gen
                base = generator.hover_visual_gen(prompt, tool, u1)
                if "Video" in tool:
                    video = generator.hover_video_gen(prompt, base, timer)
                    st.video(video)
                else:
                    st.image(base)

# --- MODULE 3: STORY REEL CREATOR ---
elif mode == "Story Reel Creator":
    st.header("Proprietary Story Sequencer")
    story_prompt = st.text_area("Describe the cinematic story (e.g., 'A journey through a neon forest ending in a city'):")
    if st.button("🎬 GENERATE FULL STORY"):
        with st.spinner("Synthesizing Multi-Scene Temporal Pixels..."):
            # Generates the base vision
            scene = generator.hover_visual_gen(story_prompt, "Text-to-Video")
            # Compiles into a long-form reel
            final_story = generator.hover_video_gen(story_prompt, scene, 30)
            if final_story:
                st.video(final_story)
                st.success("Cinematic Story Generated Successfully.")
