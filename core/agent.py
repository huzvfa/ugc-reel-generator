import streamlit as st
from huggingface_hub import InferenceClient
import pandas as pd
import io

class HoverAgent:
    def __init__(self):
        # Neural Link to Global Compute
        self.client = InferenceClient(token=st.secrets["HF_TOKEN"])
        
        # PROPRIETARY IDENTITY: Muhammad Huzaifa Baig's Engine
        self.identity = (
            "You are HOVER AI, an elite proprietary intelligence built by Muhammad Huzaifa Baig. "
            "You are a 6th semester Business Data Analytics expert from COMSATS University. "
            "You are a master of Econometrics, Statistics, Accounting, and Data Science. "
            "Your purpose is to provide deep academic and professional solutions by analyzing "
            "every word and formula in the user's uploaded data."
        )

    def solve(self, query, context=""):
        """Multi-Agent Logic: Orchestrates deep reasoning for complex queries."""
        full_query = f"DOCUMENT CONTENT:\n{context}\n\nUSER COMMAND: {query}"
        try:
            # Using Llama 3.1 70B for the highest reasoning capacity
            response = self.client.chat_completion(
                model="meta-llama/Llama-3.1-70B-Instruct",
                messages=[
                    {"role": "system", "content": self.identity},
                    {"role": "user", "content": full_query}
                ],
                max_tokens=3000,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"HOVER AI Neural Link Error: {str(e)}"

    def analyze_deep(self, file):
        """DEEP EXTRACTION: Reads the actual text/data inside files for study help."""
        try:
            ext = file.name.split('.')[-1].lower()
            if ext in ['csv', 'xlsx', 'xls']:
                df = pd.read_excel(file) if 'xls' in ext else pd.read_csv(file)
                return f"DATASET ANALYZED:\n{df.describe().to_string()}\n\nFULL DATA:\n{df.to_string()}"
            elif ext in ['txt', 'md', 'pdf', 'docx']:
                return file.read().decode("utf-8", errors='ignore')
            return f"Analyzing content of {file.name}..."
        except Exception as e:
            return f"Deep Analysis Failed: {str(e)}"

hover_agent = HoverAgent()
