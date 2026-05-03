# Conditional UI for UGC Studio
if "Video" in tool:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    use_voice = st.toggle("Enable Neural Voiceover & Script", value=True)
    
    if use_voice:
        script = st.text_area("Script (Auto-Sync Enabled):")
        # Magnetic Snapping Timeline
        timer = st.select_slider("Select Duration", options=[5, 10, 15, 30, 45, 60], value=15)
        
        # Tone Selection for Voiceover
        tone = st.selectbox("Tone:", ["Seductive", "Mature", "Cinematic", "Casual", "Angry"])
    st.markdown('</div>', unsafe_allow_html=True)
