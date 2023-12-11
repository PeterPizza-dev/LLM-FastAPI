from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.callbacks import wandb_tracing_enabled


def ask_qa(question: str, doc_path: str, enable_logging: bool = False):
    embeddings = OpenAIEmbeddings()
    loader = PyPDFLoader(doc_path)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=20)

    texts = splitter.split_documents(
        documents
    )
    vectordb = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
    )

    template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, 
    just say that you don't know, don't try to make up an answer. 
    Use three sentences maximum. Keep the answer as concise as possible. 
    Always say "thanks for asking!" at the end of the answer. 
    {context}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
    if enable_logging:
        with wandb_tracing_enabled():
            qa = RetrievalQA.from_chain_type(
                llm=ChatOpenAI(temperature=0.5, model='gpt-3.5-turbo'),
                chain_type="stuff",
                retriever=vectordb.as_retriever(search_type="similarity"),
                chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
            )
    else:
        qa = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(temperature=0.5, model='gpt-3.5-turbo'),
            chain_type="stuff",
            retriever=vectordb.as_retriever(search_type="similarity"),
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
        )

    return qa.run(question)
