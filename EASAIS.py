from huggingface_hub import InferenceClient
import streamlit as st
import pandas as pd
import os

st.title("SYBAU")
st.write("LOLLLLLLLLLLL")

client = InferenceClient(
    provider="featherless-ai",
    api_key=st.secrets["H_TOKEN"],
)

stream = client.chat.completions.create(
    model="Qwen/Qwen2.5-Math-7B-Instruct",
    messages=[
        {"role": "user","content": "What is the capital of France?"}
    ],
    temperature=0.1,
    max_tokens=100,
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content, end="")