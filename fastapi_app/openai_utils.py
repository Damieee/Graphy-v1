from config import settings
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

def get_llm_and_embeddings(openai_api_key: str = None):
    import os
    if openai_api_key:
        os.environ['OPENAI_API_KEY'] = openai_api_key
    elif settings.OPENAI_API_KEY:
        os.environ['OPENAI_API_KEY'] = settings.OPENAI_API_KEY
    embeddings = OpenAIEmbeddings()
    llm = ChatOpenAI(model_name="gpt-4o-mini")
    return llm, embeddings
