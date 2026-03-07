import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma  # changed import

load_dotenv()

embeddings = OpenAIEmbeddings()

vectorstore = Chroma(
    collection_name="enterprise_kb",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)