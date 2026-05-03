from gtts import gTTS

def generate_voiceover(text, output_path="output/voice.mp3"):
    tts = gTTS(text=text, lang='en', tld='us') # Clean US English accent
    tts.save(output_path)
    return output_path
