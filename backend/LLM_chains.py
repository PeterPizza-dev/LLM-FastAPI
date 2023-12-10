from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory, ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.callbacks import wandb_tracing_enabled


class ChatBot:
    def __init__(self, llm_model: str = 'gpt-3.5-turbo', memory: bool = True, enable_logging: bool = False):
        super().__init__()

        self.llm = ChatOpenAI(temperature=0.5, model=llm_model)
        self.conversation_buffer = memory
        self.init_chain(memory)
        self.enable_logging = enable_logging


    def init_chain(self, include_memory: bool):

        if include_memory:
            self.llm_chain = ConversationChain(
                llm=self.llm,
                memory=ConversationBufferWindowMemory(k=5),
            )
        else:
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "You're a very knowledgeable helper, that should help employees at LEGO. "
                        "Start all your answers, with Dear Lego Employee."
                    ),
                    ("human", "{question}"),
                ]
            )
            self.llm_chain = LLMChain(
                llm=self.llm,
                prompt=prompt,
                memory=ConversationBufferMemory()
            )

    def llm_chat_chain(self, input_prompt):
        if self.enable_logging:
            with wandb_tracing_enabled():
                response = self.llm_chain.run(input_prompt)
        else:
            response = self.llm_chain.run(input_prompt)
        return response

# main
if __name__ == "__main__":
    cbb = ChatBot()
    cbb.llm_chat_chain(input_prompt='What would you like to do?')