from llm.llm import get_llm

def writer_agent(context: str, query: str) -> str:
    llm = get_llm()

    prompt = f"""
You are an AI assistant.

Use the provided context to answer.

If context is from documents → answer from it  
If context is from web → summarize clearly  

Context:
{context}

Question:
{query}

Answer:
"""

    response = llm.invoke(prompt)

    return response.content if hasattr(response, "content") else str(response)