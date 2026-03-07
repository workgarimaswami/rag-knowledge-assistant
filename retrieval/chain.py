from .retrievers import ensemble_retriever
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import List, Dict, Any

llm = ChatOpenAI(model="gpt-4", temperature=0)

prompt = ChatPromptTemplate.from_template("""
You are an enterprise knowledge assistant. Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Always cite the source document names in your answer.

Context:
{context}

Question: {question}

Answer (with citations):
""")

def retrieve_with_scores(query: str) -> List[Document]:
    docs = ensemble_retriever.invoke(query)          # .invoke() instead of .get_relevant_documents()
    for doc in docs:
        doc.metadata['relevance_score'] = 0.9        # placeholder – you can compute actual scores
    return docs

def format_docs(docs: List[Document]) -> Dict[str, Any]:
    context_parts = []
    sources = set()
    for doc in docs:
        context_parts.append(f"Source: {doc.metadata.get('source', 'unknown')}\n{doc.page_content}")
        sources.add(doc.metadata.get('source', 'unknown'))
    context = "\n\n".join(context_parts)
    return {
        "context": context,
        "sources": list(sources),
        "relevance_scores": [doc.metadata.get('relevance_score', 0.0) for doc in docs]
    }

def rag_chain(question: str) -> Dict[str, Any]:
    docs = retrieve_with_scores(question)
    formatted = format_docs(docs)
    response = llm.invoke(prompt.format(context=formatted["context"], question=question))
    return {
        "answer": response.content,
        "sources": formatted["sources"],
        "relevance_scores": formatted["relevance_scores"]
    }