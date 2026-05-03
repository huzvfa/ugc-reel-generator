import streamlit as st
import asyncio
import os
import base64
from core.brain import hover_brain
from core import generator

st.set_page_config(page_title="HOVER AI | THE BREAKTHROUGH", layout="wide")

# --- CUSTOM CSS FOR HOVER PREVIEWS & GLOSSY UI ---
st.markdown("""
    <style>
    .stApp { background: #020202; color: #fff; }
    .voice-card:hover { border: 1px solid #00f2fe; cursor: crosshair; }
    /* NSFW Popup Styling */
    .nsfw-box { background: rgba(255, 0, 0, 0.1); border: 1px solid red; padding: 20px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- GLOBAL VOICE AGENTS ---
VOICES = {
    "English Male": "en-US-ChristopherNeural",
    "English Female": "en-US-AnaNeural",
    "Urdu Female": "ur-PK-UzmaNeural",
    "Urdu Male": "ur-PK-AsadNeural"
}

with st.sidebar:
    st.markdown("<h1 style='color:#00f2fe;'>💠 HOVER AI</h1>", unsafe_allow_html=True)
    app_mode = st.radio("Neural Stream:", ["Neural Chat", "UGC Studio"])

# --- FEATURE 1: NEURAL CHAT (With Document Analysis) ---
if app_mode == "Neural Chat":
    st.header("Proprietary Neural Link")
    doc = st.file_uploader("Upload Document (Excel, PDF, CSV, Text) for Analysis", type=['csv', 'xlsx', 'txt'])
    doc_context = ""
    if doc:
        doc_context = hover_brain.analyze_document(doc)
        st.success(f"HOVER AI has analyzed {doc.name}")

    if "msgs" not in st.session_state: st.session_state.msgs = []
    for m in st.session_state.msgs:
        with st.chat_message(m["role"]): st.write(m["content"])
    
    if q := st.chat_input("Ask Hover AI anything..."):
        st.session_state.msgs.append({"role": "user", "content": q})
        with st.chat_message("user"): st.write(q)
        with st.chat_message("assistant"):
            res = hover_brain.think(q, context=doc_context)
            st.write(res)
            st.session_state.msgs.append({"role": "assistant", "content": res})

# --- FEATURE 2: UGC STUDIO (Motion & NSFW Dialog) ---
elif app_mode == "UGC Studio":
    st.header("Hover Production Suite")
    
    # NSFW Detection Simulation
    nsfw_trigger = any(word in st.session_state.get('last_prompt', '').lower() for word in ['18+', 'nsfw', 'adult'])
    if nsfw_trigger and not st.session_state.get('is_18_verified'):
        st.warning("⚠️ NSFW CONTENT DETECTED")
        if st.button("I am 18+ and wish to proceed"):
            st.session_state.is_18_verified = True
            st.rerun()
        st.stop()

    col1, col2 = st.columns([1, 1])
    with col1:
        tool = st.selectbox("Tool:", ["Text-to-Video", "Image-to-Video", "Text-to-Image", "Image-to-Image"])
        prompt = st.text_area("Hover Engine Instructions:")
        st.session_state.last_prompt = prompt
        
        if "Video" in tool:
            use_script = st.toggle("Enable Neural Voiceover", value=True)
            if use_script:
                script = st.text_area("Script:")
                timer = st.slider("Duration (s):", 5, 30, 10)
                
                # PREVIEW LOGIC
                agent = st.selectbox("Select Agent (Hover to Preview):", list(VOICES.keys()))
                tone_slider = st.select_slider("Tone Tone:", options=["Soft", "Serious", "Charming", "Angry", "Seductive"])
                
                # Automatic Preview when selection changes (simulates hover response)
                with st.spinner("Refining Voice..."):
                    asyncio.run(generator.hover_voice_engine("Hey, I'm Hover AI, created to assist you.", VOICES[agent], "output/p.mp3"))
                    st.audio("output/p.mp3")

    with col2:
        if st.button("🚀 EXECUTE HOVER ENGINE", use_container_width=True):
            with st.spinner("Processing Breakthrough..."):
                base_img = generator.hover_visual_gen(prompt, tool)
                if "Video" in tool:
                    video_path = generator.hover_video_gen(prompt, base_img, timer)
                    if video_path:
                        st.video(video_path)
                else:
                    st.image(base_img)
