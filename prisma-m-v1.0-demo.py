from huggingface_hub import InferenceClient
import streamlit as st
import pandas as pd
import os
import time
from pathlib import Path
from PIL import Image
from pix2text import Pix2Text, merge_line_texts
import streamlit.components.v1 as components

def stop_stream():
    st.session_state.stop = True

st.title("PRISMA-M-V1.0 DEMO")

Docu = Path(".data")
Docu.mkdir(exist_ok=True)
local_files=[f.name for f in Docu.iterdir() if f.is_file()]

if 'exam' not in st.session_state:
    st.session_state.exam = []

if 'solution' not in st.session_state:
    st.session_state.solution = []

if 'ready_solution' not in st.session_state:
    st.session_state.ready_solution = []

if "unified_text" not in st.session_state:
    st.session_state.unified_text=""

if "edited_text" not in st.session_state:
    st.session_state.edited_text = "\n".join(st.session_state.ready_solution)
    
if "input" not in st.session_state:
    st.session_state.input = []

if "stop" not in st.session_state:
    st.session_state.stop = True

def stop_stream():
    st.session_state.stop = True


choose_exam = st.selectbox("Choose your paper", local_files)
st.session_state.exam = choose_exam

if st.session_state.ready_solution == []:
    st.session_state.solution = st.file_uploader("Upload Your Solutions", type="jpg",accept_multiple_files=True)
            
if st.button("Next") and st.session_state.ready_solution == []:
    for p in st.session_state.solution:
        p2t = Pix2Text.from_config()
        outs2 = p2t.recognize(p, file_type='text_formula', return_text=True, save_analysis_res='mixed-out.jpg')
        st.session_state.ready_solution.append(outs2)
    for k in st.session_state.ready_solution:
        st.session_state.unified_text+=f"{k}\n"

if st.session_state.unified_text != [] and st.session_state.input == []:
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.edited_text = st.text_area("Preview", value=st.session_state.unified_text, height=300)
    with col2:
        st.write(st.session_state.edited_text)
    if st.button("Confirm"):
        st.session_state.input = st.session_state.edited_text
        client = InferenceClient(
        provider="featherless-ai",
        api_key=os.environ["APITOKEN"],
        )

        stream = client.chat.completions.create(
        model="Qwen/Qwen2.5-Math-1.5B-Instruct",
        messages=[
            {"role": "system","content": "Solve the problem concisely"},
            {"role": "system","content": st.session_state.input}
        ],
        temperature=0.1,
        max_tokens=1000,
        stream=True,
        )
        left, right = st.columns([1, 10])
        left.write("🤗")
        ph = right.empty()
        text = ""
        for chunk in stream:
            delta = chunk.choices[0].delta.get("content")  # the actual string
            if delta:  
                text += delta
                ph.write(text)
        st.button("Stop", key="stop_button", on_click=stop_stream)
            if st.session_state.stop:
                break

                
        



