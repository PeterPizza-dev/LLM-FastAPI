'''
This frontend is based is based on streamlits own tutorials
and isnpired from this:
https://github.com/streamlit/llm-examples/blob/main/Chatbot.py
'''

import requests

from openai import OpenAI
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Don't have an OpenAI API key? Get one](https://platform.openai.com/account/api-keys)"

# Streamlit app
st.title("Lego case interview - LLM")
st.caption("Streamlit chatbot using OpenAI LLM - chatgpt 3.5")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

llm_endpoint = "http://localhost:8000/generate"

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # We could do som authorisation to our backend here
    #client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    #response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    #msg = response.choices[0].message.content
    response = requests.post(llm_endpoint, json={"prompt": prompt})

    if response.status_code == 200:
        msg = response.json().get("result")
    else:
        st.error(f"Error communicating with LLM. Status code: {response.status_code}")

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)