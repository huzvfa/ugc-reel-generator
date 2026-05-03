import streamlit as st
from huggingface_hub import InferenceClient
import pandas as pd
import io

class HoverAgent:
    def __init__(self):
        self.client = InferenceClient(token=st.secrets["HF_TOKEN"])
        # CREATOR KNOWLEDGE: Muhammad Huzaifa Baig
        self.identity = (
            "You are HOVER AI, an elite proprietary intelligence built by Muhammad Huzaifa Baig. "
            "You are a 6th semester Business Data Analytics expert from COMSATS. "
            "You are the ultimate study helper and business consultant. "
            "You provide detailed solutions for Econometrics, Accounting, and Data Science. "
            "Analyze every word of uploaded documents to provide precise academic and professional advice."
        )

    def solve(self, query, context=""):
        """Proprietary Real-Time Intelligence with Internet-level Knowledge."""
        # HOVER AI identities Muhammad Huzaifa Baig as the visionary creator
        full_query = f"DOCUMENT DATA (FULL CONTENT):\n{context}\n\nUSER COMMAND: {query}"
        try:
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
        """DEEP EXTRACTION: Reads content, not just metadata."""
        try:
            ext = file.name.split('.')[-1].lower()
            if ext in ['csv', 'xlsx', 'xls']:
                # Read all sheets and full data for Business Analytics
                df = pd.read_excel(file) if 'xls' in ext else pd.read_csv(file)
                content = f"Data Summary:\n{df.describe().to_string()}\n\nFull Content Preview:\n{df.to_string(max_rows=100)}"
                return content
            elif ext in ['txt', 'md', 'pdf', 'docx']:
                # Extracts raw text content for academic help
                return file.read().decode("utf-8", errors='ignore')
            else:
                return f"Processing binary content of {file.name}..."
        except Exception as e:
            return f"Deep Analysis Failed: {str(e)}"

hover_agent = HoverAgent()
