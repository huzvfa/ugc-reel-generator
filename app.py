import streamlit as st
import asyncio
import os
import base64
from core.brain import hover_brain
from core import generator

st.set_page_config(page_title="HOVER AI STUDIO", layout="wide")

# --- UI STYLING ---
st.markdown("""
    <style>
    .stApp { background: #010101; color: #fff; }
    .glass-panel { background: rgba(255,255,255,0.02); border: 1px solid #00f2fe33; border-radius: 15px; padding: 20px; }
    .download-overlay {
        position: absolute; top: 10px; right: 10px; z-index: 1000;
        background: rgba(0, 242, 254, 0.3); backdrop-filter: blur(5px);
        padding: 5px 10px; border-radius: 8px; border: 1px solid #00f2fe;
        color: white; text-decoration: none; font-size: 11px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def get_dl_link(file_path, label):
    with open(file_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f'<a href="data:application/octet-stream;base64,{data}" download="{os.path.basename(file_path)}" class="download-overlay">📥 DOWNLOAD {label}</a>'

# --- VOICE AGENTS & TONES ---
VOICES = {
    "English Male": "en-US-ChristopherNeural",
    "English Female": "en-US-AnaNeural",
    "Urdu Female (Soft)": "ur-PK-UzmaNeural",
    "Urdu Male (Soft)": "ur-PK-AsadNeural"
}

with st.sidebar:
    st.markdown("<h1 style='color:#00f2fe;'>💠 HOVER AI</h1>", unsafe_allow_html=True)
    mode = st.radio("Switch Module", ["Neural Chat", "UGC Studio"])

if mode == "Neural Chat":
    st.header("Proprietary Neural Link")
    doc = st.file_uploader("Analyze Document (Accounting, Statistics, etc.)", type=['csv', 'xlsx', 'txt'])
    ctx = hover_brain.analyze_doc(doc) if doc else ""
    
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])
    
    if q := st.chat_input("Speak to Hover AI..."):
        st.session_state.messages.append({"role": "user", "content": q})
        with st.chat_message("user"): st.write(q)
        with st.chat_message("assistant"):
            res = hover_brain.think(q, context=ctx)
            st.write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

elif mode == "UGC Studio":
    st.header("Hover Production Suite")
    
    # --- NSFW VERIFICATION DIALOG ---
    if any(x in st.session_state.get('last_p', '').lower() for x in ['18+', 'nsfw', 'adult']):
        if not st.session_state.get('verified'):
            st.warning("⚠️ NSFW CONTENT DETECTED")
            if st.button("Confirm I am 18+"):
                st.session_state.verified = True
                st.rerun()
            st.stop()

    col1, col2 = st.columns([1, 1])
    
    # Initialize variables to prevent NameError
    timer = 15
    use_script = False
    v_agent = "English Male"
    script = ""

    with col1:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        tool = st.selectbox("Select Mode:", ["Text-to-Image", "Text-to-Video", "Image-to-Video", "Image-to-Image"])
        prompt = st.text_area("Hover Engine Instructions:")
        st.session_state.last_p = prompt
        
        # --- CONDITIONAL UI FOR VIDEO MODES ---
        if "Video" in tool:
            use_script = st.toggle("Enable Voiceover & Script Function", value=True)
            if use_script:
                script = st.text_area("Script Content:")
                timer = st.select_slider("Select Duration (s):", options=[5, 10, 15, 30, 45, 60], value=15)
                v_agent = st.selectbox("Voiceover Agent:", list(VOICES.keys()))
                tone = st.select_slider("Tone:", options=["Soft", "Serious", "Charming", "Seductive", "Angry"])
                
                # Auto-Preview Hover Logic
                with st.spinner("Neural Preview..."):
                    asyncio.run(generator.hover_voice_engine("Hey, I'm Hover AI, created to assist you.", VOICES[v_agent], "output/p.mp3"))
                    st.audio("output/p.mp3")

        u1 = st.file_uploader("Primary Image", type=['png','jpg']) if "Image-" in tool else None
        u2 = st.file_uploader("Reference (Face/Body)", type=['png','jpg']) if tool == "Image-to-Image" else None
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if st.button("🚀 EXECUTE HOVER ENGINE", use_container_width=True):
            with st.spinner("Processing Breakthrough..."):
                base_img = generator.hover_generate_visual(prompt, tool, u1, u2)
                
                if "Video" in tool:
                    video_path = generator.hover_generate_video(prompt, base_img, timer)
                    if video_path:
                        st.markdown(get_dl_link(video_path, "MP4"), unsafe_allow_html=True)
                        st.video(video_path)
                else:
                    st.markdown(get_dl_link(base_img, "PNG"), unsafe_allow_html=True)
                    st.image(base_img)
