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

with st.sidebar:
    st.markdown("<h1 style='color:#00f2fe;'>💠 HOVER AI</h1>", unsafe_allow_html=True)
    mode = st.radio("Neural Interface", ["Neural Chat", "UGC Studio"])

if mode == "Neural Chat":
    st.header("Proprietary Neural Link")
    
    if "messages" not in st.session_state: 
        st.session_state.messages = []
    
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])

    # --- UNIFIED COMMAND BAR ---
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

elif mode == "UGC Studio":
    st.header("Hover Production Suite")
    # (Rest of UGC Studio remains same)
