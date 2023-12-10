from fastapi import FastAPI, Request, BackgroundTasks
import openai
import os
from data_validation import Output, InputData
from dotenv import load_dotenv, find_dotenv
import wandb
from LLM_chains import llm_chat_chain

# Initliase backend endpoint
app = FastAPI()


@app.on_event('startup')
def init_data():
    load_dotenv(find_dotenv())
    openai.api_key = os.getenv('OPENAI_API_KEY')
    run = wandb.init(project="LLM-lego", job_type="generation")
    # TODO figure out logging after RAG etc.

@app.post("/generate", response_model=Output)
def generate(request: Request, input_data: InputData):
    prompt = input_data.prompt
    response = llm_chat_chain(prompt)

    return Output(result=response)



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)