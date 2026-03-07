import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import List

load_dotenv()

# --- Dense retriever (using regular embeddings) ---
regular_embeddings = OpenAIEmbeddings()
vectorstore = Chroma(
    collection_name="enterprise_kb",
    embedding_function=regular_embeddings,
    persist_directory="./chroma_db"
)
dense_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# --- BM25 retriever (needs all documents) ---
all_docs_data = vectorstore.get()
documents = [
    Document(page_content=text, metadata=metadata)
    for text, metadata in zip(all_docs_data['documents'], all_docs_data['metadatas'])
]
bm25_retriever = BM25Retriever.from_documents(documents)
bm25_retriever.k = 5

# --- HyDE: generate hypothetical document ---
hyde_llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
hyde_prompt = PromptTemplate.from_template(
    "Please write a hypothetical document that would answer the following question: {question}"
)
hyde_chain = hyde_prompt | hyde_llm | StrOutputParser()

class HyDERetriever(BaseRetriever):
    vectorstore: Chroma
    k: int = 5

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        hypo_doc = hyde_chain.invoke({"question": query})
        return self.vectorstore.similarity_search(hypo_doc, k=self.k)

hyde_retriever = HyDERetriever(vectorstore=vectorstore, k=5)

# --- Ensemble retriever (HyDE + BM25) ---
ensemble_retriever = EnsembleRetriever(
    retrievers=[hyde_retriever, bm25_retriever],
    weights=[0.6, 0.4]
)