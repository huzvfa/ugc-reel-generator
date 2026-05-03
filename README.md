# ugc-reel-generator
# 🎬 AI-UGC Reel Generator

An automated pipeline to generate high-converting **User-Generated Content (UGC)** reels using open-source AI models.

## 🚀 Key Features
- **Zero Cost:** Uses SDXL Turbo and gTTS for free asset generation.
- **UGC Style:** Prompt engineering optimized for "Shot-on-iPhone" realism.
- **Modular Design:** Swap out models for Image Gen, Voice, or Animation easily.

## 🛠️ Technical Stack
- **Python 3.10+**
- **Diffusers (SDXL Turbo):** For ultra-fast creator image generation.
- **LivePortrait:** For realistic facial animation and lip-syncing.
- **MoviePy:** For programmatic video editing and 9:16 formatting.
- **Streamlit:** For the user dashboard.

## 📋 How to Run
1. Clone the repo: `git clone https://github.com/yourusername/ugc-reel-generator`
2. Install deps: `pip install -r requirements.txt`
3. Run the UI: `streamlit run app.py`
