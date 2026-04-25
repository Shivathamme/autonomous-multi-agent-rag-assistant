# Import types for defining structured state
from typing import TypedDict, Optional

# Import LangGraph to build workflow graph
from langgraph.graph import StateGraph, END

# Import all agents
from agents.planner import planner_agent        # decides RAG or Web
from agents.researcher import researcher_agent  # gets data from PDF (RAG)
from agents.writer import writer_agent          # generates answer
from agents.reviewer import reviewer_agent      # improves answer

# Import web search tool
from tools.web_search import web_search

# Import memory for conversation history
from memory.chat_memory import ChatMemory

# Create memory object (stores chat history)
memory = ChatMemory()


# Define the structure of data passed between nodes
class AgentState(TypedDict):
    query: str                 # user question
    task: Optional[str]        # planner decision (research / web)
    context: Optional[str]     # retrieved info (PDF or web)
    answer: Optional[str]      # generated answer
    final_answer: Optional[str]# improved final answer


# Main function to build workflow
def build_workflow(vectorstore, memory):

    # ---------------- PLANNER NODE ---------------- #
    def planner_node(state: AgentState):
        # Decide whether to use RAG or Web
        task = planner_agent(state["query"])

        # Return updated state with task
        return {**state, "task": task}


    # ---------------- RESEARCHER NODE ---------------- #
    def researcher_node(state: AgentState):
        # Get context from PDF using RAG
        context = researcher_agent(vectorstore, state["query"])

        # Debug: print retrieved context
        print("\n===== RAG CONTEXT =====\n")
        print(context[:500])   # print only first 500 chars

        # If context is weak or irrelevant → switch to web
        if not context or "Unrelated" in context or len(context.strip()) < 100:
            print("[INFO] Switching to web search...")
            context = web_search(state["query"])

        # Return updated state with context
        return {**state, "context": context}


    # ---------------- WEB NODE ---------------- #
    def web_node(state: AgentState):
        # Directly get context from web search
        context = web_search(state["query"])

        # Return updated state
        return {**state, "context": context}


    # ---------------- WRITER NODE ---------------- #
    def writer_node(state: AgentState):
        # Extract query and context
        query = state["query"]
        context = state["context"]

        # Get previous conversation history
        memory_context = memory.get_context()

        # Combine memory + current context
        full_context = f"""
Conversation History:
{memory_context}

Current Context:
{context}
"""

        # Generate answer using LLM
        answer = writer_agent(full_context, query)

        # Save current Q&A to memory
        memory.add(query, answer)

        # Return updated state with answer
        return {**state, "answer": answer}


    # ---------------- REVIEWER NODE ---------------- #
    def reviewer_node(state: AgentState):
        # Improve the generated answer (grammar, clarity)
        final_answer = reviewer_agent(state["answer"])

        # Return final improved answer
        return {**state, "final_answer": final_answer}


    # ---------------- ROUTING LOGIC ---------------- #
    def route(state: AgentState):
        # If planner says web_search → go to web node
        # else → go to researcher (RAG)
        return "web" if state["task"] == "web_search" else "researcher"


    # ---------------- BUILD GRAPH ---------------- #
    workflow = StateGraph(AgentState)

    # Add all nodes to graph
    workflow.add_node("planner", planner_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("web", web_node)
    workflow.add_node("writer", writer_node)
    workflow.add_node("reviewer", reviewer_node)

    # Set starting node (ENTRY POINT)
    workflow.set_entry_point("planner")

    # Conditional routing after planner
    workflow.add_conditional_edges(
        "planner",
        route,  # function decides next node
        {
            "researcher": "researcher",
            "web": "web",
        },
    )

    # Define flow of nodes
    workflow.add_edge("researcher", "writer")  # RAG → writer
    workflow.add_edge("web", "writer")         # Web → writer
    workflow.add_edge("writer", "reviewer")    # Writer → reviewer
    workflow.add_edge("reviewer", END)         # End workflow

    # Compile and return workflow
    return workflow.compile()