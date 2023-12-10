# LLM-FastAPI

This LLM-Application is made as a part of an interviewing round. 
The task was to make a proxy for employer promts to an LLM. 

This repository provides a proxy to an LLM, openai 3.5 - turbo, in this case. 
The app contains both a chat interface with an LLM and the posibility to upload a document and ask questions. 
The app can be tested locally using the frontend, and by curling the API. 
The backend is made with fastapi and the frontend is made using streamlit, and is based on their own tutorials
and inspired from [this repository](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py).

## Overview of the app

Maybe include above here

## Getting started 
To run the repository follow these steps
### Get an openAI API key 
1. Go to https://platform.openai.com/account/api-keys.
2. Click on the + Create new secret key button.
3. Next, enter an identifier name (optional) and click on the Create secret key button.

### Update the .env 
See the `.env_example` file and create a new file named `.env`. Include WANDB api key here if needed for logging.

### Run the app

The app can be run simply be cloning the git repository, installing the requirements 
and running:`./run_app.sh`from the terminal. 