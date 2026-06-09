# autonomous-multi-agent-rag-assistant
Autonomous multi-agent RAG system built with LangGraph that answers questions from PDFs and fetches real-time information from the web. Combines document retrieval, web search, and LLMs to deliver accurate, context-aware responses.

## 🔗 Live Demo: https://huggingface.co/spaces/ShivaThamme/autonomous-multi-agent-rag-assistant

## 🚀 Overview
This project is an AI-powered assistant that can:
- Answer questions from uploaded PDF documents
- Fetch real-time information from the web
- Use multiple AI agents to generate accurate answers

## 🧠 Architecture

User Query → Planner → (RAG or Web) → Writer → Reviewer → Final Answer

## ⚙️ Features

- 📄 PDF-based question answering (RAG)
- 🌐 Web search fallback (DuckDuckGo)
- 🤖 Multi-agent system (LangGraph)
- 🧠 Conversation memory
- 🔁 Automatic routing (RAG vs Web)

## 🏗️ Tech Stack

- LangGraph
- LangChain
- ChromaDB
- HuggingFace Embeddings
- Groq (LLaMA 3)
- Streamlit

## 📂 Project Structure

### 🔹 `app/`
Handles Streamlit UI, file uploads, and user interaction.

### 🔹 `agents/`
Contains AI agents:
- `planner.py` → decides RAG or Web  
- `researcher.py` → retrieves PDF content  
- `writer.py` → generates answers  
- `reviewer.py` → improves responses  

### 🔹 `graph/`
Defines workflow using LangGraph (agent connections and routing logic).

### 🔹 `rag/`
Implements Retrieval-Augmented Generation:
- embeddings  
- vectorstore  
- retriever  
- reranker  

### 🔹 `tools/`
External tools (e.g., web search).

### 🔹 `memory/`
Stores chat history for multi-turn conversations.

### 🔹 `utils/`
Helper functions for document loading and splitting.

### 🔹 `data/uploads/` *(ignored)*
Stores uploaded PDFs.

### 🔹 `db/` *(ignored)*
Stores vector database.


## ▶️ How to Run

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
pip install -r requirements.txt
