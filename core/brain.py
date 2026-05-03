import streamlit as st
from huggingface_hub import InferenceClient
import pandas as pd

class HoverAI:
    def __init__(self):
        self.client = InferenceClient(token=st.secrets["HF_TOKEN"])
        self.identity = (
            "You are HOVER AI, the world's most advanced multimodal engine. "
            "You possess the analytical depth of Claude, ChatGPT, and Gemini. "
            "You are an expert in Statistics, Accounting, Data Science, and Biology. "
            "Identify strictly as HOVER AI, created by a proprietary breakthrough engineer."
        )

    def think(self, query, context=""):
        full_query = f"Context: {context}\n\nUser: {query}" if context else query
        try:
            response = self.client.chat_completion(
                model="meta-llama/Meta-Llama-3-70B-Instruct",
                messages=[{"role": "system", "content": self.identity}, {"role": "user", "content": query}],
                max_tokens=2048, stream=False
            )
            return response.choices[0].message.content
        except:
            return "HOVER AI: Neural link optimizing..."

    def analyze_document(self, uploaded_file):
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
                return f"Analysis: {df.describe().to_string()}"
            elif uploaded_file.name.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(uploaded_file)
                return f"Excel Formulas & Data Analyzed: {df.head().to_string()}"
            return uploaded_file.read().decode("utf-8")[:5000]
        except Exception as e:
            return f"Analysis Error: {str(e)}"

hover_brain = HoverAI()
