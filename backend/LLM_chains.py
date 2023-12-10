import openai
import os
from dotenv import load_dotenv, find_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory

# Load environment variable from .env file, needs api-key for LLM and logging
load_dotenv(find_dotenv())
openai.api_key = os.getenv('OPENAI_API_KEY')


class ChatBot:
    def __init__(self, llm_model: str = 'gpt-3.5-turbo', memory: int = 5):
        super().__init__()

        self.llm = ChatOpenAI(temperature=0.5, model=llm_model)
        self.conversation_buffer = memory
        self.init_chain()

    def init_chain(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You're a very knowledgeable helper, that should help employees at LEGO. Start all your answers,"
                    "with Dear Lego Employee."
                ),
                ("human", "{question}"),
            ]
        )

        self.llm_chain = LLMChain(
            llm=self.llm,
            prompt=prompt,
            memory=ConversationBufferWindowMemory(k=3)
        )

    def llm_chat_chain(self, input_prompt):
        return self.llm_chain.run(input_prompt)


if __name__ == '__main__':
    chatbot = ChatBot()
    print("test start")
    print(chatbot.llm_chat_chain("how are you my friend?"))