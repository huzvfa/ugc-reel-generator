import streamlit as st
from core.image_gen import UGCImageGen
from core.voice_gen import generate_voiceover

st.title("🎬 UGC AI Reel Generator")
st.markdown("Generate AI marketing reels for free.")

prompt = st.text_input("Describe your AI Creator:", "A girl wearing a hoodie talking to camera")
script = st.text_area("What should they say?", "Check out our latest collection, link in bio!")

if st.button("Generate Reel"):
    with st.spinner("Generating Image..."):
        gen = UGCImageGen()
        img_path = gen.generate(prompt)
        st.image(img_path, caption="Generated Creator")
    
    with st.spinner("Generating Audio..."):
        audio_path = generate_voiceover(script)
        st.audio(audio_path)
    
    st.success("Now run LivePortrait script to animate!")
