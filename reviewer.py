from llm.llm import get_llm


def reviewer_agent(answer: str) -> str:
    try:
        llm = get_llm()

        prompt = f"""
Improve the answer below by:
- Making it clear and well-structured
- Fixing grammar and spelling
- Removing redundancy
- Keeping it concise and accurate

Answer:
{answer}

Improved:
"""

        response = llm.invoke(prompt)

        return response.content if hasattr(response, "content") else answer

    except:
        return answer