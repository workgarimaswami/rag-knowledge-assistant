import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .loaders import load_document
from .vector_store import vectorstore

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)

def ingest_file(file_path: str):
    """Load a file, split it, and add to the vector store."""
    print(f"Ingesting {file_path}...")
    docs = load_document(file_path)

    # Split documents into chunks
    chunks = text_splitter.split_documents(docs)

    # Add source filename to metadata
    for chunk in chunks:
        chunk.metadata["source"] = os.path.basename(file_path)

    # Add to vector store
    vectorstore.add_documents(chunks)
    vectorstore.persist()
    print(f"✅ Added {len(chunks)} chunks from {file_path}")