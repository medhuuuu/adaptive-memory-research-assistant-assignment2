from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("BERGET_API_KEY"),
    base_url="https://api.berget.ai/v1"
)

def get_ai_response(prompt):

    response = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",

    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.7,
    max_tokens=500
    )
    return response.choices[0].message.content


