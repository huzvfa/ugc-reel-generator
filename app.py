# ... [Your Neon CSS and Layout from before] ...

if st.button("🚀 Generate Final Content"):
    with st.spinner("AI Engine Working..."):
        # 1. Generate the Image Base
        if "Image-to" in mode or "Image-Video" in mode:
            if not uploaded_file: st.error("Please upload an image!"); st.stop()
            img_path = generator.query_im2im_gen(uploaded_file, prompt)
        else:
            img_path = generator.query_image_gen(prompt)
        
        # 2. Handle Video Mode
        if "Video" in mode:
            # Generate Voiceover
            audio_path = asyncio.run(generator.generate_voice(script, voices[selected_voice], "output/final_voice.mp3"))
            
            # Create the 30s Reel (Image + Voice + Motion Effect)
            video_path = generator.create_ugc_video(img_path, audio_path, video_duration)
            
            if video_path:
                st.video(video_path)
                st.success(f"30-Second AI Reel Generated successfully!")
        else:
            # Just show the image if not in video mode
            st.image(img_path, caption="Generated UGC Image", use_column_width=True)
