# LLM-FastAPI

This LLM-Application is made as a part of an interviewing round. 
The task was to make a proxy for employer promts to an LLM. 

This repository provides a proxy to an LLM, openai 3.5 - turbo, in this case. 
The app contains both a chat interface with an LLM and the posibility to upload a document and ask questions about it. 
The app can be tested locally using the frontend, and by calls to the API. 
The backend is made with fastapi and the frontend is made using streamlit, and is based on their own tutorials
and inspired from [this repository](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py).

## Getting started 
To run the repository follow these steps
### Get an openAI API key 
1. Go to https://platform.openai.com/account/api-keys.
2. Click on the + Create new secret key button.
3. Next, enter an identifier name (optional) and click on the Create secret key button.

### Update the .env 
See the `.env_example` file and create a new file named `.env`. Include WANDB api key here if needed for logging.

### Running the basic app
To run the basic app from the root, run `uvicorn backend.app:app --log-config=log_conf.yaml`.
The app endpoints can the be pinged, like this:
1. **Generate**: `curl -X POST -H "Content-Type: application/json" -d '{"prompt":"Str"}' http://127.0.0.1:8000/generate`
2. **DocQ&A**: `curl -X POST -H "Content-Type: application/json" -d '{"prompt":"Str","path":"Str"}' http://127.0.0.1:8000/doc_prompt`


### Run the app w. frontend

The app can be run simply be cloning the git repository, installing the requirements 
and running: `./run_app.sh`from the terminal, and the streamlit dashboard should open up.

### Logging with WANDB
The app can be run with logged responsens to WANDB, for tracking and development.
To enable this set `log=True` in `/backend/app.py`, and add your wandb api key to the .env file. 
Logging is done using LangChains `wandb_tracing_enabled` and is currently a bit unstable, and sometimes times out.
Thus, it is disabled by default. 
