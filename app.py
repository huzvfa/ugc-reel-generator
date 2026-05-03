import streamlit as st
import asyncio
import os
from core.brain import hover_brain
from core import generator

st.set_page_config(page_title="HOVER AI | THE BREAKTHROUGH", layout="wide")

# --- GLOBAL SETTINGS ---
VOICES = {
    "Male (English)": "en-US-ChristopherNeural",
    "Female (English)": "en-US-AnaNeural",
    "Female (Urdu)": "ur-PK-UzmaNeural",
    "Male (Urdu)": "ur-PK-AsadNeural"
}

st.markdown("<style>.stApp { background: #020202; color: #fff; }</style>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h1 style='color:#00f2fe;'>💠 HOVER AI</h1>", unsafe_allow_html=True)
    app_mode = st.radio("Neural Link:", ["Neural Chat", "UGC Studio"])

# --- MODULE 1: NEURAL CHAT (Full Field Analysis) ---
if app_mode == "Neural Chat":
    st.header("Proprietary Neural Link")
    doc = st.file_uploader("Upload Data (Excel/CSV/Text)", type=['csv', 'xlsx', 'txt'])
    context = hover_brain.analyze_document(doc) if doc else ""
    
    if "msgs" not in st.session_state: st.session_state.msgs = []
    for m in st.session_state.msgs:
        with st.chat_message(m["role"]): st.write(m["content"])
    
    if q := st.chat_input("Analyze with Hover AI..."):
        st.session_state.msgs.append({"role": "user", "content": q})
        with st.chat_message("user"): st.write(q)
        with st.chat_message("assistant"):
            res = hover_brain.think(q, context=context)
            st.write(res)
            st.session_state.msgs.append({"role": "assistant", "content": res})

# --- MODULE 2: UGC STUDIO (Motion & Fixed Scoping) ---
elif app_mode == "UGC Studio":
    st.header("Hover Production Suite")
    
    # NSFW Verification
    if any(x in st.session_state.get('p_check', '').lower() for x in ['nsfw', '18+']):
        if not st.session_state.get('is_adult'):
            st.warning("⚠️ 18+ Content Detected. Confirm your age to proceed.")
            if st.button("I am 18+"):
                st.session_state.is_adult = True
                st.rerun()
            st.stop()

    col1, col2 = st.columns([1, 1])
    # Default values to prevent NameError
    timer = 10 
    script = ""
    agent = "Male (English)"

    with col1:
        tool = st.selectbox("Tool:", ["Text-to-Video", "Image-to-Video", "Text-to-Image", "Image-to-Image"])
        prompt = st.text_area("Instructions:")
        st.session_state.p_check = prompt
        
        if "Video" in tool:
            use_voice = st.toggle("Enable Neural Voiceover", value=True)
            if use_voice:
                script = st.text_area("Script:")
                timer = st.slider("Duration (s):", 5, 30, 15)
                agent = st.selectbox("Agent:", list(VOICES.keys()))
                
                # Instant Neural Preview
                with st.spinner("Neural Sync..."):
                    asyncio.run(generator.hover_voice_engine("Hey, I'm Hover AI, created to assist you.", VOICES[agent], "output/p.mp3"))
                    st.audio("output/p.mp3")

    with col2:
        u1 = st.file_uploader("Reference", type=['png','jpg']) if "Image-" in tool else None
        if st.button("🚀 EXECUTE HOVER ENGINE", use_container_width=True):
            with st.spinner("Processing..."):
                base_img = generator.hover_visual_gen(prompt, tool, u1)
                if "Video" in tool:
                    # Timer is now safely defined
                    video_path = generator.hover_video_gen(prompt, base_img, timer)
                    if script:
                        audio = asyncio.run(generator.hover_voice_engine(script, VOICES[agent], "output/a.mp3"))
                        # Note: Add a function to sync audio/video if needed here
                    st.video(video_path)
                else:
                    st.image(base_img)
