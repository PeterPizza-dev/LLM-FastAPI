from fastapi import FastAPI, Request
import logging
import os
from dotenv import load_dotenv, find_dotenv
from backend.data_validation import Output, InputData, InputDataWPdf
from backend.LLM_chains import ChatBot
from backend.simple_retrieval import ask_qa
import sys
logger = logging.getLogger(__name__)


load_dotenv(find_dotenv())
log = False  # Setup logging, currently logging times out.

# Check API key exits in .env file else kill app
try:
    os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
except:
    logger.info("Please provide valid OpenAI API key in .env and relaunch app")
    sys.exit(1)


if log:
    # If logging check valid api key
    try:
        os.environ['WANDB_API_KEY'] = os.getenv('WANDB_API_KEY')
    except:
        logger.info("Please provide valid WANDB API key in .env and relaunch app")
        sys.exit(1)

    os.environ["LANGCHAIN_WANDB_TRACING"] = "true"
    os.environ["WANDB_PROJECT"] = "langchain-tracing"

# Initialise app
app = FastAPI()


# Initialise chains
bot = ChatBot(enable_logging=log)


@app.get("/")
def root():
    return {"message": "Version 1.0 of LLM app"}


@app.post("/doc_prompt")
def doc_prompt(request: Request, input_data: InputDataWPdf):
    prompt = input_data.prompt
    input_path = input_data.path
    response = ask_qa(prompt, input_path, enable_logging=log)
    return Output(result=response)


@app.post("/generate", response_model=Output)
def generate(request: Request, input_data: InputData):
    prompt = input_data.prompt
    response = bot.llm_chat_chain(prompt)
    return Output(result=response)
