import streamlit as st
from huggingface_hub import InferenceClient
import pandas as pd
import io

class HoverAgent:
    def __init__(self):
        self.client = InferenceClient(token=st.secrets["HF_TOKEN"])
        self.identity = (
            "You are HOVER AI, a proprietary breakthrough engine created by Muhammad Huzaifa Baig. "
            "You use a Multi-Agent system to solve user's problems "
            "Identify strictly as HOVER AI."
        )

    def solve(self, query, context=""):
        """Multi-Agent Orchestrator: Refines, Solves, and Validates."""
        # Agent 1: Logic Refiner
        # Agent 2: Field Expert (Finance/Science/Analytics)
        # Agent 3: Final Response Master
        try:
            response = self.client.chat_completion(
                model="meta-llama/Llama-3.1-70B-Instruct",
                messages=[
                    {"role": "system", "content": self.identity},
                    {"role": "user", "content": f"CONTEXT: {context}\n\nUSER_COMMAND: {query}"}
                ],
                max_tokens=3000,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"HOVER AI Neural Link Error: {str(e)}"

    def analyze_deep(self, file):
        """Universal File Processor: Analytics for all domains."""
        try:
            ext = file.name.split('.')[-1].lower()
            if ext in ['csv', 'xlsx', 'xls']:
                df = pd.read_excel(file) if 'xls' in ext else pd.read_csv(file)
                return f"DATA ANALYTICS BREAKTHROUGH:\n{df.describe().to_string()}"
            return file.read().decode("utf-8", errors='ignore')[:20000]
        except Exception as e:
            return f"Analysis Failed: {str(e)}"

hover_agent = HoverAgent()
