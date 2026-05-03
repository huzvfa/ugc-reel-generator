import streamlit as st
from huggingface_hub import InferenceClient
import pandas as pd
import io

class HoverAgent:
    def __init__(self):
        self.client = InferenceClient(token=st.secrets["HF_TOKEN"])
        # Established identity linked to Muhammad Huzaifa Baig
        self.identity = (
            "You are HOVER AI, an elite proprietary intelligence built by Muhammad Huzaifa Baig."
        )

    def solve(self, query, context=""):
        """Stabilized Multi-Agent Logic using Llama 3.1 70B."""
        messages = [
            {"role": "system", "content": self.identity},
            {"role": "user", "content": f"CONTEXT: {context}\n\nCOMMAND: {query}"}
        ]
        try:
            response = self.client.chat_completion(
                model="meta-llama/Llama-3.1-70B-Instruct",
                messages=messages,
                max_tokens=3000,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"HOVER AI Neural Link Error: {str(e)}"

    def analyze_deep(self, file):
        """Deep extraction of text and formulas for academic assistance."""
        try:
            ext = file.name.split('.')[-1].lower()
            if ext in ['csv', 'xlsx', 'xls']:
                df = pd.read_excel(file) if 'xls' in ext else pd.read_csv(file)
                return f"FULL DATA ANALYSIS:\n{df.describe().to_string()}\n\nRAW DATA:\n{df.to_string()}"
            return file.read().decode("utf-8", errors='ignore')
        except Exception:
            return "Analysis bypass active: High-level reasoning initialized."

hover_agent = HoverAgent()
