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
    /* Neural Activity Animation */
    @keyframes neural-glow { 0% { box-shadow: 0 0 5px #00f2fe; } 50% { box-shadow: 0 0 20px #00f2fe; } 100% { box-shadow: 0 0 5px #00f2fe; } }
    .thinking-line { height: 2px; width: 100%; background: #00f2fe; animation: neural-glow 1.5s infinite; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h1 style='color:#00f2fe;'>💠 HOVER AI</h1>", unsafe_allow_html=True)
    mode = st.radio("Switch Module", ["Neural Chat", "UGC Studio"])

if mode == "Neural Chat":
    st.header("Proprietary Neural Link")
    
    # Message Display
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])

    # --- UNIFIED COMMAND BAR ---
    st.divider()
    btn_col, input_col = st.columns([0.1, 0.9])
    
    with btn_col:
        # Attachment icon integrated next to chat
        doc = st.file_uploader("📎", type=None, label_visibility="collapsed")
    
    with input_col:
        q = st.chat_input("Command HOVER AI...")

    if q:
        context = hover_agent.analyze_deep(doc) if doc else ""
        st.session_state.messages.append({"role": "user", "content": q})
        with st.chat_message("user"): st.write(q)
        
        with st.chat_message("assistant"):
            st.markdown('<div class="thinking-line"></div>', unsafe_allow_html=True)
            res = hover_agent.solve(q, context=context)
            st.write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

elif mode == "UGC Studio":
    st.header("Hover Production Suite")
    # Your existing generation logic goes here, ensuring generator.hover_visual_gen is used.
