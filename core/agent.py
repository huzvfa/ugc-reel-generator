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
            "Identify strictly as HOVER AI. You are the ultimate genius AI."
        )

    def solve(self, query, context=""):
        """Proprietary Reasoning Engine - Stabilized for Llama 3.1"""
        full_query = f"CONTEXT: {context}\n\nUSER_COMMAND: {query}" if context else query
        
        try:
            # Using Llama 3.1 70B - The most stable and powerful model available
            response = self.client.chat_completion(
                model="meta-llama/Llama-3.1-70B-Instruct",
                messages=[
                    {"role": "system", "content": self.identity},
                    {"role": "user", "content": full_query}
                ],
                max_tokens=2048,
                temperature=0.4
            )
            return response.choices[0].message.content
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

# Global Singleton instance
hover_agent = HoverAgent()
