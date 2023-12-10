import streamlit as st
import tempfile
import requests

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Don't have an OpenAI API key? Get one](https://platform.openai.com/account/api-keys)"

st.title("File Q&A")
uploaded_file = st.file_uploader("Upload a document", type=("pdf")) # for now just supports pdf
question = st.text_input(
    "Ask something about the uploaded document",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if uploaded_file and question and not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")

llm_endpoint = "http://localhost:8000/doc_prompt"


if uploaded_file and question and openai_api_key:
    # Call a function here that reads and returns a vector store or similar path
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    # Call one endpoint with path here
    response = requests.post(llm_endpoint, json={"prompt": question, "path": tmp_file_path})

    if response.status_code == 200:
        msg = response.json().get("result")
    else:
        st.error(f"Error communicating with LLM. Status code: {response.status_code}")
        msg = 'error'

    st.chat_message("assistant", avatar='frontend/assets/AIhead.jpeg').write(msg)
