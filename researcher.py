from rag.retriever import get_retriever
from rag.reranker import rerank_documents


def researcher_agent(vectorstore, query: str) -> str:
    try:
        retriever = get_retriever(vectorstore)

        # 🔹 Step 1: Retrieve relevant docs
        docs = retriever.invoke(query)


        # 🔥 IMPORTANT FIX:
        # If no relevant docs → return EMPTY
        if not docs or len(docs) == 0:
            print("[INFO] No relevant documents found → fallback to WEB")
            return ""

        # 🔹 Step 2: Rerank docs
        docs = rerank_documents(docs, query)

        # 🔹 Step 3: Build context
        context = "\n\n".join([doc.page_content for doc in docs])

        # 🔍 DEBUG
        print("\n===== FINAL CONTEXT =====\n")
        print(context[:1000])

        return context

    except Exception as e:
        print("Researcher error:", e)
        return ""