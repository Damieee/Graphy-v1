import os
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

def get_llm_and_embeddings(openai_api_key: str):
    os.environ['OPENAI_API_KEY'] = openai_api_key
    embeddings = OpenAIEmbeddings()
    llm = ChatOpenAI(model_name="gpt-4o")
    return llm, embeddings
