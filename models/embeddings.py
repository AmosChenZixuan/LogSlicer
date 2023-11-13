import os

from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings import SentenceTransformerEmbeddings

from dotenv import load_dotenv
load_dotenv()


class EmbeddingsFactory:
    @staticmethod
    def create(embeddings_type):
        if embeddings_type == 'openai':
            return get_openai_embeddings()
        elif embeddings_type == 'azure':
            return get_azure_openai_embeddings()
        elif embeddings_type == 'sentran':
            return get_sentence_transformer_embeddings()

def get_openai_embeddings():
    return OpenAIEmbeddings(openai_api_key=os.getenv("CHATGPT_API_KEY"))

def get_azure_openai_embeddings():
    return OpenAIEmbeddings(openai_api_key=os.getenv("AZURE_API_KEY"),
                            deployment=os.getenv("AZURE_EMBEDDING_DEPLOY_NAME"),
                            model=os.getenv("AZURE_EMBEDDING_DEPLOY_NAME"),
                            openai_api_base=os.getenv("AZURE_API_BASE"),
                            openai_api_type="azure") 

def get_sentence_transformer_embeddings():
    return SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")