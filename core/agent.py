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
        """Proprietary Reasoning Engine - Zero-Footprint Stability"""
        full_query = f"CONTEXT: {context}\n\nUSER_COMMAND: {query}" if context else query
        try:
            # Using the most stable 2026 method to stop the 'Bad Request' cycle
            response = self.client.chat_completion(
                model="meta-llama/Meta-Llama-3-70B-Instruct",
                messages=[
                    {"role": "system", "content": self.identity},
                    {"role": "user", "content": full_query}
                ],
                max_tokens=2048,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            # Direct error reporting to identify exactly what is failing
            return f"HOVER AI Neural Link Error: {str(e)}"

    def analyze_deep(self, file):
        """Processes all file types including Excel, CSV, and Text"""
        try:
            ext = file.name.split('.')[-1].lower()
            if ext in ['csv', 'xlsx', 'xls']:
                df = pd.read_excel(file) if 'xls' in ext else pd.read_csv(file)
                return f"DATA ANALYSIS:\n{df.describe().to_string()}"
            return file.read().decode("utf-8", errors='ignore')[:15000]
        except Exception as e:
            return f"Analysis Failed: {str(e)}"

# Global Singleton instance
hover_agent = HoverAgent()
