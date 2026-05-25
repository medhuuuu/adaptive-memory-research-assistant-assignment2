import chromadb

client = chromadb.PersistentClient(
    path="chroma_db"
)

chat_collection = client.get_or_create_collection(
    name="chat_memory"
)

pdf_collection = client.get_or_create_collection(
    name="pdf_memory"
)

# ===============================================
# ---------------- CHAT MEMORY ------------------
# ===============================================

def store_chat_memory(text, embedding):

    chat_collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=[str(hash(text))]
    )

def retrieve_chat_memory(query_embedding):

    results = chat_collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    return results["documents"][0]



# ==============================================
# ---------------- PDF MEMORY ------------------
# ==============================================

def store_pdf_chunk(text, embedding):

    pdf_collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=[str(hash(text))]
    )

def retrieve_pdf_chunks(query_embedding):

    results = pdf_collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    return results["documents"][0]


def clear_pdf_collection():

    global pdf_collection

    try:

        ids = pdf_collection.get()["ids"]

        if ids:

            pdf_collection.delete(ids=ids)

    except Exception as e:

        print("Error clearing PDF collection:", e)