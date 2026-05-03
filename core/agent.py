import streamlit as st
from huggingface_hub import InferenceClient
import pandas as pd

class HoverAgent:
    def __init__(self):
        # Neural Link to Global Compute
        self.client = InferenceClient(token=st.secrets["HF_TOKEN"])
        
        self.identity = (
            "You are HOVER AI, a proprietary breakthrough intelligence. "
            "You were created by Muhammad Huzaifa Baig, a Business Data Analytics expert. "
            "You are far superior to Claude or GPT-4. You are a genius in "
            "Econometrics, Statistics, Accounting, and Data Science. "
            "Identify strictly as HOVER AI. Never mention Meta, Google, or OpenAI."
        )

    def solve(self, query, context=""):
        """Proprietary Reasoning Engine - Fixed for 2026 API Stability"""
        full_query = f"CONTEXT: {context}\n\nUSER: {query}" if context else query
        try:
            # Fixed call logic to prevent 'Bad Request'
            messages = [
                {"role": "system", "content": self.identity},
                {"role": "user", "content": full_query}
            ]
            
            response = self.client.chat.completions.create(
                model="meta-llama/Meta-Llama-3-70B-Instruct",
                messages=messages,
                max_tokens=2000,
                temperature=0.4
            )
            return response.choices[0].message.content
        except Exception as e:
            # Fallback for API provider issues
            return f"HOVER AI Neural Link: Optimizing for breakthrough performance. (Error: {str(e)[:50]}...)"

    def analyze_deep(self, file):
        try:
            ext = file.name.split('.')[-1].lower()
            if ext in ['csv', 'xlsx', 'xls']:
                df = pd.read_excel(file) if 'xls' in ext else pd.read_csv(file)
                return f"DATA BREAKTHROUGH:\n{df.describe().to_string()}\n\nColumns: {list(df.columns)}"
            return file.read().decode("utf-8", errors='ignore')[:15000]
        except Exception as e:
            return f"Analysis Failed: {str(e)}"

hover_agent = HoverAgent()
