import requests
import streamlit as st

# Using Hugging Face's Free Inference API
API_URL = "https://api-inference.huggingface.co/models/stabilityai/sdxl-turbo"
headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"} 

def query_image_gen(prompt):
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    return response.content # This returns the raw image data
