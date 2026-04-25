from langchain_chroma import Chroma
from rag.embeddings import get_embeddings


def create_vectorstore(chunks, persist_dir="db"):
    if not chunks:
        raise ValueError("❌ No chunks provided to create vectorstore")

    embeddings = get_embeddings()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir
    )

    return vectorstore


def load_vectorstore(persist_dir="db"):
    embeddings = get_embeddings()

    return Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings
    )