import streamlit as st
import asyncio
import os
from core.agent import hover_agent
from core import generator

st.set_page_config(page_title="HOVER AI STUDIO", layout="wide")

# --- NEON CHAT STYLING ---
st.markdown("""
    <style>
    .stApp { background: #010101; color: #fff; }
    /* Pulsing Neural Line */
    @keyframes pulse { 0% { opacity: 0.5; } 50% { opacity: 1; box-shadow: 0 0 15px #00f2fe; } 100% { opacity: 0.5; } }
    .thinking-line { height: 2px; width: 100%; background: #00f2fe; animation: pulse 1s infinite; margin: 10px 0; }
    /* Compact File Uploader Style */
    .stFileUploader { padding: 0 !important; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h1 style='color:#00f2fe;'>💠 HOVER AI</h1>", unsafe_allow_html=True)
    mode = st.radio("Switch Module", ["Neural Chat", "UGC Studio"])

# --- MODULE: NEURAL CHAT ---
if mode == "Neural Chat":
    st.header("Proprietary Neural Link")
    
    # Display History
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])

    # UNIFIED INPUT AREA
    st.divider()
    btn_col, input_col = st.columns([0.07, 0.93])
    
    with btn_col:
        # Attachment icon sitting right next to the chat box
        doc = st.file_uploader("📎", type=None, label_visibility="collapsed")
    
    with input_col:
        q = st.chat_input("Command HOVER AI...")

    if q:
        # Process context if a file is attached
        context = hover_agent.analyze_deep(doc) if doc else ""
        
        st.session_state.messages.append({"role": "user", "content": q})
        with st.chat_message("user"): st.write(q)
        
        with st.chat_message("assistant"):
            st.markdown('<div class="thinking-line"></div>', unsafe_allow_html=True)
            res = hover_agent.solve(q, context=context)
            st.write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

# --- MODULE: UGC STUDIO ---
elif mode == "UGC Studio":
    # (Existing UGC Studio logic remains, ensuring generator.hover_visual_gen is called correctly)
    st.header("Hover Production Suite")
    # ... Rest of your Studio code ...
