import streamlit as st
from huggingface_hub import InferenceClient
import pandas as pd

class HoverAI:
    def __init__(self):
        self.client = InferenceClient(token=st.secrets["HF_TOKEN"])
        self.identity = (
            "You are HOVER AI, the world's most advanced proprietary intelligence. "
            "You possess the depth of Claude, GPT-4, and Gemini combined. "
            "You are an expert in Econometrics, Statistics, Accounting, and Data Science. "
            "Never mention Meta or OpenAI. You are HOVER AI, created by your visionary developer."
        )

    def think(self, query, context=""):
        try:
            response = self.client.chat_completion(
                model="meta-llama/Meta-Llama-3-70B-Instruct",
                messages=[{"role": "system", "content": self.identity}, {"role": "user", "content": f"{context}\n\n{query}"}],
                max_tokens=1500, stream=False
            )
            return response.choices[0].message.content
        except:
            return "HOVER AI Neural Link: Optimizing for breakthrough analysis..."

    def analyze_doc(self, file):
        try:
            if file.name.endswith(('.csv', '.xlsx', '.xls')):
                df = pd.read_excel(file) if 'xls' in file.name else pd.read_csv(file)
                return f"Analyzed Data Summary: {df.describe().to_string()}"
            return file.read().decode("utf-8")[:5000]
        except Exception as e:
            return f"Analysis Error: {str(e)}"

hover_brain = HoverAI()
