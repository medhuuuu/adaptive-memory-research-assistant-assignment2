from src.chatbot import get_ai_response

def summarize_memory(memory_text):

    prompt = f"""
    Summarize this conversation memory briefly:

    {memory_text}
    """

    summary = get_ai_response(prompt)

    return summary