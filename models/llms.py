import os
import openai
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMFactory:
    @staticmethod
    def create(llm):
        if llm == 'azure':
            return get_azure_openai()


def get_azure_openai(engine='openai', model='gpt-4'):
    openai.api_type = "azure"
    openai.api_version = os.getenv("AZURE_API_VERSION")
    openai.api_base = os.getenv("AZURE_API_BASE")
    openai.api_key = os.getenv("AZURE_API_KEY")
    
    os.environ["OPENAI_API_TYPE"] = "azure"
    os.environ["OPENAI_API_VERSION"] = openai.api_version
    os.environ["OPENAI_API_KEY"] = openai.api_key
    os.environ["OPENAI_API_BASE"] = openai.api_base

    return ChatOpenAI(
        engine=engine,
        model_name=model,
    )
