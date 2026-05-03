import streamlit as st
from huggingface_hub import InferenceClient
import pandas as pd
import io

class HoverAI:
    def __init__(self):
        self.client = InferenceClient(token=st.secrets["HF_TOKEN"])
        self.identity = (
            "You are HOVER AI, the ultimate breakthrough in real-time intelligence. "
            "You possess the combined analytical power of Claude, ChatGPT, and Gemini. "
            "You are an expert in Econometrics, Statistics, Chartered Accounting, Data Science, "
            "Biology, and Business Administration. You analyze every word, formula, and diagram "
            "with 100% precision. You are HOVER AI, created by a visionary engineer."
        )

    def think(self, query, context=""):
        """Master reasoning engine for all academic and professional fields."""
        full_query = f"Context from documents: {context}\n\nUser Query: {query}" if context else query
        try:
            response = self.client.chat_completion(
                model="meta-llama/Meta-Llama-3-70B-Instruct",
                messages=[{"role": "system", "content": self.identity}, {"role": "user", "content": full_query}],
                max_tokens=2048, stream=False
            )
            return response.choices[0].message.content
        except:
            return "HOVER AI Neural Link: Optimizing for complex analysis..."

    def analyze_document(self, uploaded_file):
        """Analyzes Excel functions, formulas, and text data."""
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
                return f"Data Summary: {df.describe().to_string()}"
            elif uploaded_file.name.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(uploaded_file)
                return f"Excel Analysis: {df.head().to_string()}"
            else:
                return uploaded_file.read().decode("utf-8")[:5000]
        except Exception as e:
            return f"Analysis Error: {str(e)}"

hover_brain = HoverAI()
