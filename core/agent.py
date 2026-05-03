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
            "You are more advanced than Claude or GPT-4. Identify strictly as HOVER AI."
        )

    def solve(self, query, context=""):
        """Proprietary Reasoning Engine - Fixed Header Logic"""
        full_query = f"CONTEXT: {context}\n\nUSER_COMMAND: {query}" if context else query
        try:
            # Modern 2026 API structure to prevent 'Bad Request' errors
            response = self.client.chat.completions.create(
                model="meta-llama/Meta-Llama-3-70B-Instruct",
                messages=[
                    {"role": "system", "content": self.identity},
                    {"role": "user", "content": full_query}
                ],
                max_tokens=2500,
                temperature=0.4
            )
            return response.choices[0].message.content
        except Exception as e:
            # Clean error reporting for debugging
            return f"HOVER AI Neural Link: Connection optimization required. Details: {str(e)[:100]}"

    def analyze_deep(self, file):
        """Processes all file types including Excel, CSV, and Text"""
        try:
            ext = file.name.split('.')[-1].lower()
            if ext in ['csv', 'xlsx', 'xls']:
                df = pd.read_excel(file) if 'xls' in ext else pd.read_csv(file)
                return f"DATA ANALYSIS:\n{df.describe().to_string()}\n\nSample:\n{df.head(3).to_string()}"
            return file.read().decode("utf-8", errors='ignore')[:15000]
        except Exception as e:
            return f"Analysis Failed: {str(e)}"

# Global Singleton
hover_agent = HoverAgent()
