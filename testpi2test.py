from pix2text import Pix2Text, merge_line_texts


p2t = Pix2Text.from_config()
outs2 = p2t.recognize("image.png", file_type='text_formula', return_text=True, save_analysis_res='mixed-out.jpg')
st.session_state.edited_text = st.text_area("Editable Preview", value=st.session_state.unified_text, height=300)


        client = InferenceClient(
            provider="featherless-ai",
            api_key=os.environ["APITOKEN"],
        )

        stream = client.chat.completions.create(
            model="Qwen/Qwen2.5-Math-1.5B-Instruct",
            messages=[
                {"role": "system","content": "Solve the problem concisely"},
                {"role": "system","content": str(st.session_state.edited_text)}
            ],
            temperature=0.1,
            max_tokens=1000,
            stream=True,
        )

        for chunk in stream:
            delta = chunk.choices[0].delta.get("content")
            if delta:
                left, right = st.columns([1, 10])
                left.write("🤗")
                ph = right.empty()
                text = ""
                d = chunk.choices[0].delta.content
                text += d.replace("\n", " ")
                ph.write(text)
                time.sleep(0.5)