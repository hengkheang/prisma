import os
from huggingface_hub import InferenceClient
import streamlit as st
import pandas as pd

client = InferenceClient(
    provider="featherless-ai",
    api_key=os.environ["_TOKEN"],
)

stream = client.chat.completions.create(
    model="Qwen/Qwen2.5-Math-7B-Instruct",
    messages=[
        {"role": "user","content": "What is the capital of France?"}
    ],
    temperature=0.1,
    max_tokens=1000,
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content, end="")