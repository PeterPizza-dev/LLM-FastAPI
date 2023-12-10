import logging
from fastapi import FastAPI, Request
import sys

import openai
import os
from dotenv import load_dotenv, find_dotenv
from backend.data_validation import Output, InputData, InputDataWPdf
from backend.LLM_chains import ChatBot
from backend.simple_retrieval import ask_qa


load_dotenv(find_dotenv())
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialise app
app = FastAPI()


# Initialise chains
bot = ChatBot()


@app.post("/api_key")
def api_key_missing(request: Request):
    return api_key_missing


@app.get("/")
def root():
    return {"message": "Version 1.0 of LLM app"}


@app.post("/doc_prompt")
def doc_prompt(request: Request, input_data: InputDataWPdf):
    prompt = input_data.prompt
    input_path = input_data.path
    response = ask_qa(prompt, input_path)
    return Output(result=response)


@app.post("/generate", response_model=Output)
def generate(request: Request, input_data: InputData):
    prompt = input_data.prompt
    response = bot.llm_chat_chain(prompt)
    return Output(result=response)
