import streamlit as st
import os

from src.chatbot import get_ai_response

from src.embeddings import create_embedding

from src.memory_manager import (
    store_chat_memory,
    retrieve_chat_memory,
    store_pdf_chunk,
    retrieve_pdf_chunks,
    clear_pdf_collection
)

from src.pdf_handler import (
    extract_text_from_pdf
)

from src.retriever import (
    split_text
)

# ================= PAGE CONFIG ================= #

st.set_page_config(
    page_title="Adaptive Memory Assistant",
    page_icon="🧠",
    layout="wide"
)

# ================= SESSION STATE ================= #

if "chat_history" not in st.session_state:

    st.session_state.chat_history = []

# ================= SIDEBAR ================= #

with st.sidebar:

    st.title("🧠 Adaptive Memory Assistant")

    st.write("""
    Hybrid AI assistant with:
    - Adaptive Memory
    - PDF Research Support
    - Semantic Retrieval
    - Conversational Context
    """)

    st.divider()

    uploaded_file = st.file_uploader(
        "📄 Upload PDF",
        type="pdf"
    )

# ================= PDF PROCESSING ================= #

if uploaded_file:
    
    # Clear previous PDF vectors
    clear_pdf_collection()
    
    os.makedirs(
        "data/uploaded_pdfs",
        exist_ok=True
    )

    save_path = os.path.join(
        "data/uploaded_pdfs",
        uploaded_file.name
    )

    with open(save_path, "wb") as f:

        f.write(uploaded_file.getbuffer())

    st.sidebar.success("PDF uploaded!")

    # Extract PDF text
    pdf_text = extract_text_from_pdf(
        save_path
    )

    # Split text into chunks
    chunks = split_text(
        pdf_text,
        chunk_size=1500
    )

    # Store chunks in vector DB
    for chunk in chunks:

        embedding = create_embedding(
            chunk
        )

        store_pdf_chunk(
            chunk,
            embedding
        )

    st.sidebar.success(
        "PDF processed successfully!"
    )

# ================= MAIN TITLE ================= #

st.title("🧠 Adaptive Memory Research Assistant")

st.caption(
    "Memory-aware AI with PDF research capabilities"
)

# ================= DISPLAY CHAT HISTORY ================= #

for sender, message in st.session_state.chat_history:

    if sender == "You":

        with st.chat_message("user"):

            st.write(message)

    else:

        with st.chat_message("assistant"):

            st.write(message)

# ================= CHAT INPUT ================= #

user_input = st.chat_input(
    "Ask something..."
)

# ================= USER QUERY ================= #

if user_input:

    # Show user message immediately
    with st.chat_message("user"):

        st.write(user_input)

    # Create embedding
    query_embedding = create_embedding(
        user_input
    )

    # ================= MEMORY RETRIEVAL ================= #

    try:

        relevant_memories = retrieve_chat_memory(
            query_embedding
        )

        memory_context = "\n".join(
            relevant_memories
        )

    except:

        memory_context = ""

    # ================= PDF RETRIEVAL ================= #

    try:

        relevant_pdf_chunks = retrieve_pdf_chunks(
            query_embedding
        )

        pdf_context = "\n".join(
            relevant_pdf_chunks
        )

    except:

        pdf_context = ""

    # ================= PROMPT ================= #

    full_prompt = f"""
    Chat Memory:
    {memory_context}

    PDF Context:
    {pdf_context}

    Current User Question:
    {user_input}

    Instructions:
    - Answer naturally
    - Prioritize PDF information if available
    - Use memory if relevant
    - If answer comes from PDF, mention it
    - If information is unclear, say so
    """

    # ================= AI RESPONSE ================= #

    response = get_ai_response(
        full_prompt
    )

    # Show AI response
    with st.chat_message("assistant"):

        st.write(response)

    # Save chat history
    st.session_state.chat_history.append(
        ("You", user_input)
    )

    st.session_state.chat_history.append(
        ("AI", response)
    )

    # ================= STORE MEMORY ================= #

    memory_text = f"""
    User: {user_input}

    AI: {response}
    """

    memory_embedding = create_embedding(
        memory_text
    )

    store_chat_memory(
        memory_text,
        memory_embedding
    )