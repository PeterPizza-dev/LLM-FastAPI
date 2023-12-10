from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
import openai
import os
from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import ChatOpenAI

# Load environment variable from .env file, needs api-key for LLM and logging
load_dotenv(find_dotenv())
openai.api_key = os.getenv('OPENAI_API_KEY')
embeddings = OpenAIEmbeddings()


def get_vector_db_one_document(path):
    loader = PyPDFLoader(path)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20)

    texts = splitter.split_documents(
        documents
    )
    vectordb = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory="db"
    )
    vectordb.persist() # This stores the db in the specified folder
    return vectordb


def ask_qa(question, doc_path):
    vectordb = get_vector_db_one_document(doc_path)
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(temperature=0.5,
                    model='gpt-3.5-turbo'),
        chain_type="stuff",
        retriever=vectordb.as_retriever()
    )
    return qa.run(question)
