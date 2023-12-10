import logging
from fastapi import FastAPI, Request
import wandb # TODO figure out if we use this, if not --> DELETE

from backend.data_validation import Output, InputData, InputDataWPdf
from backend.LLM_chains import ChatBot
from backend.simple_retrieval import ask_qa


# Initialise app
app = FastAPI()

# Initialise chains
bot = ChatBot()

logging.info("Running here when we start ###################################")

# @app.on_event('startup') # TODO delete this if we can not make it work
# def init_data():
#     # Create class here that holds llm-chains
#
#     load_dotenv(find_dotenv())
#     openai.api_key = os.getenv('OPENAI_API_KEY')
#     run = wandb.init(project="LLM-lego", job_type="generation")
#     # TODO figure out logging after RAG etc.


@app.get("/")
async def root():
    return {"message": "Version 1.0 of LLM app"}


@app.post("/doc_prompt")
async def doc_prompt(request: Request, input_data: InputDataWPdf):
    prompt = input_data.prompt
    input_path = input_data.path
    response = ask_qa(prompt, input_path)
    return Output(result=response)


@app.post("/generate", response_model=Output)
async def generate(request: Request, input_data: InputData):
    prompt = input_data.prompt
    response = bot.llm_chat_chain(prompt)
    return Output(result=response)
