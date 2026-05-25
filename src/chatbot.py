from openai import OpenAI
import streamlit as st

client = OpenAI(
    api_key=st.secrets["BERGET_API_KEY"],
    base_url="https://api.berget.ai/v1"
)

def get_ai_response(prompt):

    try:

        response = client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            max_tokens=300
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"API Error: {str(e)}"