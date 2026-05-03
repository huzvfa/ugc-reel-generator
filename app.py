import streamlit as st
import asyncio
import os
import base64
from core.brain import hover_brain
from core import generator

st.set_page_config(page_title="HOVER AI | THE BREAKTHROUGH", layout="wide")

# --- CUSTOM CSS: Glossy UI & Neural Responsiveness ---
st.markdown("""
    <style>
    .stApp { background: #020202; color: #fff; }
    .glass-card { background: rgba(255,255,255,0.02); border: 1px solid #00f2fe44; border-radius: 15px; padding: 25px; }
    /* NSFW Popup Styling */
    .nsfw-dialog { background: rgba(255, 0, 0, 0.1); border: 1px solid red; padding: 20px; border-radius: 10px; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- VOICE AGENTS ---
VOICES = {
    "Male (English)": "en-US-ChristopherNeural",
    "Female (English)": "en-US-AnaNeural",
    "Female (Urdu - Soft)": "ur-PK-UzmaNeural",
    "Male (Urdu - Soft)": "ur-PK-AsadNeural"
}

with st.sidebar:
    st.markdown("<h1 style='color:#00f2fe;'>💠 HOVER AI</h1>", unsafe_allow_html=True)
    app_mode = st.radio("Neural Link:", ["Neural Chat", "UGC Studio"])

# --- MODULE 1: NEURAL CHAT (Advanced Analysis) ---
if app_mode == "Neural Chat":
    st.header("Proprietary Neural Link")
    doc = st.file_uploader("Upload Document for Analysis (Excel, CSV, PDF)", type=['csv', 'xlsx', 'txt'])
    doc_context = ""
    if doc:
        doc_context = hover_brain.analyze_document(doc)
        st.success(f"HOVER AI has analyzed {doc.name}")

    if "msgs" not in st.session_state: st.session_state.msgs = []
    for m in st.session_state.msgs:
        with st.chat_message(m["role"]): st.write(m["content"])
    
    if q := st.chat_input("Speak to HOVER AI..."):
        st.session_state.msgs.append({"role": "user", "content": q})
        with st.chat_message("user"): st.write(q)
        with st.chat_message("assistant"):
            res = hover_brain.think(q, context=doc_context)
            st.write(res)
            st.session_state.msgs.append({"role": "assistant", "content": res})

# --- MODULE 2: UGC STUDIO (Motion & NSFW Logic) ---
elif app_mode == "UGC Studio":
    st.header("Hover Production Suite")
    
    # NSFW Verification Logic
    is_nsfw = any(x in st.session_state.get('p_check', '').lower() for x in ['nsfw', '18+', 'adult', 'naked', 'seductive'])
    if is_nsfw and not st.session_state.get('over_18'):
        st.markdown('<div class="nsfw-dialog"><h3>⚠️ Age Verification Required</h3><p>HOVER AI has detected potential 18+ content. Are you over 18?</p></div>', unsafe_allow_html=True)
        if st.button("Confirm: I am 18+"):
            st.session_state.over_18 = True
            st.rerun()
        st.stop()

    col1, col2 = st.columns([1, 1])
    with col1:
        tool = st.selectbox("Tool:", ["Text-to-Video", "Image-to-Video", "Text-to-Image", "Image-to-Image"])
        prompt = st.text_area("Instructions:")
        st.session_state.p_check = prompt
        
        if "Video" in tool:
            use_voice = st.toggle("Enable Neural Voiceover & Script", value=True)
            if use_voice:
                script = st.text_area("Script:")
                timer = st.slider("Duration (s):", 5, 30, 10)
                agent = st.selectbox("Voice Agent:", list(VOICES.keys()))
                tone = st.select_slider("Tone:", options=["Soft", "Serious", "Charming", "Seductive", "Angry"])
                
                # Real-time Preview: Runs when selection changes
                with st.spinner("Neural Preview..."):
                    preview_text = "Hey, I'm Hover AI, created to assist you."
                    asyncio.run(generator.hover_voice_engine(preview_text, VOICES[agent], "output/p.mp3"))
                    st.audio("output/p.mp3")

    with col2:
        u1 = st.file_uploader("Reference", type=['png','jpg']) if "Image-" in tool else None
        if st.button("🚀 EXECUTE HOVER ENGINE", use_container_width=True):
            with st.spinner("Processing Breakthrough..."):
                base_img = generator.hover_visual_gen(prompt, tool, u1)
                if "Video" in tool:
                    video_path = generator.hover_video_gen(prompt, base_img, timer)
                    if video_path:
                        st.video(video_path)
                else:
                    st.image(base_img)
