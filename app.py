import streamlit as st
import asyncio
import os
import base64
from core.brain import hover_brain
from core import generator

st.set_page_config(page_title="HOVER AI | THE BREAKTHROUGH", layout="wide")

# --- GLOSSY DOWNLOAD SYSTEM ---
def download_media(file_path, type="Video"):
    with open(file_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    color = "#00f2fe" if type == "Video" else "#f200fe"
    return f'''
        <div style="position: relative;">
            <a href="data:application/octet-stream;base64,{data}" 
               download="{os.path.basename(file_path)}" 
               style="position: absolute; top: 10px; right: 10px; z-index: 999; 
                      background: {color}; color: white; padding: 5px 12px; 
                      border-radius: 8px; text-decoration: none; font-size: 12px; 
                      font-weight: bold; border: 1px solid white;">
               📥 DOWNLOAD {type.upper()}
            </a>
        </div>
    '''

# --- UI LAYOUT ---
with st.sidebar:
    st.title("💠 HOVER AI")
    app_mode = st.radio("Interface:", ["Neural Chat", "Production Suite"])

if app_mode == "Neural Chat":
    st.header("Proprietary Neural Link")
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])
    if q := st.chat_input("Speak to HOVER AI..."):
        st.session_state.messages.append({"role": "user", "content": q})
        with st.chat_message("user"): st.write(q)
        with st.chat_message("assistant"):
            res = hover_brain.think(q)
            st.write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

elif app_mode == "Production Suite":
    st.header("Hover Production Suite")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        tool = st.selectbox("Tool:", ["Text-to-Video", "Image-to-Video", "Text-to-Image", "Image-to-Image"])
        prompt = st.text_area("Hover Engine Instructions:")
        
        # CONDITIONAL VIDEO UI
        if "Video" in tool:
            script = st.text_area("Voiceover Script (Optional):")
            timer = st.slider("Duration (s):", 5, 30, 10)
            v_agent = st.selectbox("Agent:", ["en-US-AnaNeural", "en-GB-RyanNeural", "ur-PK-UzmaNeural"])
            
        u1 = st.file_uploader("Upload Image", type=['jpg','png']) if "Image-" in tool else None

    with col2:
        if st.button("🚀 EXECUTE HOVER ENGINE", use_container_width=True):
            with st.spinner("Processing..."):
                # 1. Generate Base Vision
                base_img = generator.hover_generate_visual(prompt, tool, u1)
                
                if "Video" in tool:
                    # 2. GENERATE REAL VIDEO
                    video_path = generator.hover_generate_video(prompt, base_img, timer)
                    if video_path:
                        st.markdown(download_media(video_path, "Video"), unsafe_allow_html=True)
                        st.video(video_path)
                else:
                    # 3. GENERATE IMAGE
                    st.markdown(download_media(base_img, "Image"), unsafe_allow_html=True)
                    st.image(base_img)
