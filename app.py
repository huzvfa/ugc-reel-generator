import streamlit as st
import asyncio
import os
import base64
from core import generator

st.set_page_config(page_title="HOVER AI | BREAKTHROUGH", layout="wide")

# --- GLOSSY DOWNLOAD OVERLAY CSS ---
st.markdown("""
    <style>
    .stApp { background: #010101; color: #fff; }
    .glass-panel { background: rgba(255,255,255,0.02); border: 1px solid #00f2fe44; border-radius: 20px; padding: 25px; }
    .download-btn {
        position: absolute; top: 10px; right: 10px; z-index: 100;
        background: rgba(0, 242, 254, 0.2); backdrop-filter: blur(5px);
        padding: 8px; border-radius: 8px; border: 1px solid #00f2fe;
        color: white; text-decoration: none; font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# Helper for Download Icon
def get_download_link(file_path, label="Download"):
    with open(file_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f'<a href="data:application/octet-stream;base64,{data}" download="{os.path.basename(file_path)}" class="download-btn">📥 {label}</a>'

# --- HOVER CONTROL ---
with st.sidebar:
    st.title("💠 HOVER AI")
    mode = st.selectbox("Module", ["Neural Chat", "UGC Studio"])

if mode == "Neural Chat":
    st.header("Proprietary Neural Link")
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])
    if q := st.chat_input("Speak to HOVER AI..."):
        st.session_state.messages.append({"role": "user", "content": q})
        with st.chat_message("user"): st.write(q)
        with st.chat_message("assistant"):
            res = generator.hover_neural_chat(q)
            st.write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

elif mode == "UGC Studio":
    st.header("Hover Production Suite")
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        tool = st.selectbox("Select Tool:", ["Text-to-Image", "Image-to-Image", "Text-to-Video", "Image-to-Video"])
        prompt = st.text_area("Hover Engine Instructions:")
        
        # --- CONDITIONAL TOOLS (Only for Video) ---
        if "Video" in tool:
            use_voice = st.toggle("Enable Neural Voice & Script", value=True)
            if use_voice:
                script = st.text_area("Script:")
                timer = st.slider("Duration (s):", 5, 30, 10)
                v_agent = st.selectbox("Agent:", ["en-US-AnaNeural", "en-GB-RyanNeural", "ur-PK-UzmaNeural"])
        
        u1 = st.file_uploader("Primary Image", type=['jpg','png']) if "Image-" in tool else None
        u2 = st.file_uploader("Reference (Face/Body)", type=['jpg','png']) if tool == "Image-to-Image" else None

    with col2:
        if st.button("🚀 EXECUTE HOVER ENGINE", use_container_width=True):
            with st.spinner("Processing Breakthrough..."):
                # 1. Base Visual Generation
                vis_path = generator.hover_visual_engine(prompt, tool, u1, u2)
                
                if "Video" in tool:
                    # 2. REAL AI MOTION
                    motion = generator.hover_motion_engine(prompt, vis_path)
                    final_path = motion if motion else vis_path
                    
                    if use_voice and script:
                        audio = asyncio.run(generator.hover_voice_gen(script, v_agent, "output/a.mp3"))
                        final_path = generator.hover_sync_master(final_path, audio, timer)
                    
                    # 3. VIDEO OUTPUT WITH DOWNLOAD OVERLAY
                    st.markdown(get_download_link(final_path, "Video"), unsafe_allow_html=True)
                    st.video(final_path)
                else:
                    # 3. IMAGE OUTPUT WITH DOWNLOAD OVERLAY
                    st.markdown(get_download_link(vis_path, "Image"), unsafe_allow_html=True)
                    st.image(vis_path)
    st.markdown('</div>', unsafe_allow_html=True)
