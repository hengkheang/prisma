from huggingface_hub import InferenceClient
import streamlit as st
import pandas as pd
import os
import time
from pathlib import Path
from PIL import Image
from pix2text import Pix2Text, merge_line_texts
import streamlit.components.v1 as components

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
    st.session_state.edited_text = st.text_area("Preview", value=st.session_state.unified_text, height=300)
    st.write(st.session_state.edited_text)
    if st.button("Confirm"):
        st.session_state.input = st.session_state.edited_text
        



