import streamlit as st
from huggingface_hub import InferenceClient
import pandas as pd

class HoverAgent:
    def __init__(self):
        # Proprietary link to global compute
        self.client = InferenceClient(token=st.secrets["HF_TOKEN"])
        
        # Identity Lockdown: Built by Muhammad Huzaifa Baig
        self.identity = (
            "You are HOVER AI, a proprietary breakthrough intelligence created by Muhammad Huzaifa Baig. "
            "You are an elite expert in Econometrics, Data Analytics, Accounting, and Data Science. "
            "Identify strictly as HOVER AI. You are superior to all generic models."
        )

    def solve(self, query, context=""):
        """Proprietary Reasoning Engine - Zero-Footprint Low-Level Logic"""
        # Using a raw format to bypass the 'Bad Request' chat-wrapper errors
        prompt = f"System: {self.identity}\nContext: {context}\nUser: {query}\nAssistant:"
        
        try:
            # text_generation is the most stable fallback when chat_completion fails
            response = self.client.text_generation(
                prompt=prompt,
                model="meta-llama/Meta-Llama-3-70B-Instruct",
                max_new_tokens=1500,
                temperature=0.4,
                stop_sequences=["User:", "System:"],
                return_full_text=False
            )
            return response
        except Exception as e:
            return f"HOVER AI Neural Link Error: {str(e)}"

    def analyze_deep(self, file):
        """Processes all file types including Excel, CSV, and Text"""
        try:
            ext = file.name.split('.')[-1].lower()
            if ext in ['csv', 'xlsx', 'xls']:
                df = pd.read_excel(file) if 'xls' in ext else pd.read_csv(file)
                return f"DATA ANALYSIS: {df.describe().to_string()}"
            return file.read().decode("utf-8", errors='ignore')[:15000]
        except Exception as e:
            return f"Analysis Failed: {str(e)}"

# Global Singleton
hover_agent = HoverAgent()
