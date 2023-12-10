import requests
import streamlit as st
import os

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Don't have an OpenAI API key? Get one](https://platform.openai.com/account/api-keys)"
    # set os .env variable first if needed
    os.environ['OPENAI_API_KEY'] = openai_api_key


# Streamlit app
st.title("Lego case interview - LLM")
st.caption("Streamlit chatbot using OpenAI LLM - chatgpt 3.5")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?", }]

for msg in st.session_state.messages:
    st.chat_message(msg["role"], avatar='frontend/assets/AIhead.jpeg').write(msg["content"])

llm_endpoint = "http://localhost:8000/generate"

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # We could do som authorisation to our backend here
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar='frontend/assets/worker.png').write(prompt)
    response = requests.post(llm_endpoint, json={"prompt": prompt})

    if response.status_code == 200:
        msg = response.json().get("result")
    else:
        st.error(f"Error communicating with LLM. Status code: {response.status_code}")
        msg = 'error'

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant", avatar='frontend/assets/AIhead.jpeg').write(msg)