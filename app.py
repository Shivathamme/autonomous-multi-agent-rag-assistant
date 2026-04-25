import sys
import os
import re

# Fix import path
sys.path.insert(0, os.getcwd())
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st

from utils.loader import load_documents
from utils.splitter import split_documents
from rag.vectorstore import create_vectorstore
from graph.workflow import build_workflow

# ---------------- SETUP ---------------- #

os.makedirs("data/uploads", exist_ok=True)
os.makedirs("db", exist_ok=True)

st.set_page_config(page_title="AI Autonomous RAG Assistant", layout="wide")
st.title("🤖 Autonomous Multi-Agent RAG Assistant")

# ---------------- SESSION STATE ---------------- #

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    from memory.chat_memory import ChatMemory
    st.session_state.memory = ChatMemory()

if "current_db" not in st.session_state:
    st.session_state.current_db = None

memory = st.session_state.memory

# ---------------- FILE UPLOAD ---------------- #

uploaded_files = st.file_uploader(
    "Upload PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

# ---------------- PROCESS DOCUMENTS ---------------- #

if uploaded_files:
    if st.button("Process Documents"):
        with st.spinner("Processing documents..."):

            file_paths = []

            for file in uploaded_files:
                file_path = f"data/uploads/{file.name}"
                with open(file_path, "wb") as f:
                    f.write(file.read())
                file_paths.append(file_path)

            docs = load_documents(file_paths)
            chunks = split_documents(docs)

            # 🔥 Safe DB name
            safe_name = "_".join([
                re.sub(r'[^a-zA-Z0-9]', '_', f.name) for f in uploaded_files
            ])
            db_path = f"db/{safe_name}"

            vectorstore = create_vectorstore(chunks, persist_dir=db_path)

            # Save state
            st.session_state.vectorstore = vectorstore
            st.session_state.current_db = db_path

            # Reset chat + memory
            st.session_state.messages = []
            from memory.chat_memory import ChatMemory
            st.session_state.memory = ChatMemory()

            st.success("✅ Documents processed successfully!")

# ---------------- DISPLAY CHAT ---------------- #

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- CHAT INPUT ---------------- #

query = st.chat_input("Ask a question...")

# ---------------- PROCESS QUERY ---------------- #

if query:

    # Show user message
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    with st.chat_message("user"):
        st.markdown(query)

    with st.spinner("Thinking... 🤖"):

        # 🔥 IMPORTANT: allow vectorstore = None
        workflow = build_workflow(
            st.session_state.vectorstore,
            memory
        )

        result = workflow.invoke({"query": query})
        answer = result.get("final_answer", "No response generated.")

    # Show assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    with st.chat_message("assistant"):
        st.markdown(answer)

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("⚙️ Controls")

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    from memory.chat_memory import ChatMemory
    st.session_state.memory = ChatMemory()

if st.session_state.current_db:
    st.sidebar.info(f"📄 Active DB: {st.session_state.current_db}")
else:
    st.sidebar.info("🌐 Mode: Web Only (No PDF)")
