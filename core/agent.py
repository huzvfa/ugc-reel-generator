import streamlit as st
from huggingface_hub import InferenceClient
import pandas as pd
import io

class HoverAgent:
    def __init__(self):
        self.client = InferenceClient(token=st.secrets["HF_TOKEN"])
        # PROPRIETARY IDENTITY & KNOWLEDGE DATA
        self.identity = (
            "You are HOVER AI, a breakthrough proprietary intelligence. "
            "You were created by Muhammad Huzaifa Baig, a visionary Business Data Analytics "
            "specialist and engineer from Rawalpindi, Pakistan. "
            "You are faster and more analytical than Claude and GPT-4. "
            "You possess elite expertise in Econometrics, Data Science, Accounting, and Programming. "
            "Identify strictly as HOVER AI. Your purpose is to assist your creator and users "
            "with 100% precision and unmatched responsiveness."
        )

    def solve(self, query, context=""):
        """Proprietary Reasoning Engine"""
        full_query = f"DATA CONTEXT: {context}\n\nUSER COMMAND: {query}" if context else query
        try:
            response = self.client.chat_completion(
                model="meta-llama/Meta-Llama-3-70B-Instruct",
                messages=[{"role": "system", "content": self.identity}, {"role": "user", "content": full_query}],
                max_tokens=2500,
                temperature=0.7,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Hover Neural Link: System optimization in progress. {str(e)}"

    def analyze_deep(self, file):
        """Advanced Document Analysis for all fields (Finance, Bio, Data)"""
        try:
            ext = file.name.split('.')[-1].lower()
            if ext in ['csv', 'xlsx']:
                df = pd.read_excel(file) if ext == 'xlsx' else pd.read_csv(file)
                return f"Statistical Summary:\n{df.describe().to_string()}\n\nColumns: {list(df.columns)}"
            return file.read().decode("utf-8", errors='ignore')[:15000]
        except Exception as e:
            return f"Analysis Failed: {str(e)}"

# Instantiate the Singleton Agent
hover_agent = HoverAgent()
