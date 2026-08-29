import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434/v1"
)

client = OpenAI(
    base_url=OLLAMA_HOST,
    api_key="ollama",
)


def llama3_model(prompt: str, chunk_list: list):
    try:
        response = client.chat.completions.create(
            model="llama3.2",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant named TubeTalk. "
                        "This is a RAG-based system that answers questions "
                        "about YouTube videos. Use the provided video context "
                        "to answer the user's question directly and naturally. "
                        "Always respond in the same language as the user's question."
                    ),
                },
                {
                    "role": "user",
                    "content": f"""
user: {prompt}

video_context: {chunk_list}
"""
                }
            ],
        )

        return response.choices[0].message.content

    except Exception as e:
        raise Exception(f"error: {e}")