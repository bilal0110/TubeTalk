import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def detect_language(text: str) -> str:
    """
    Detect the language of the user's question.

    Returns:
        "English" for English questions
        "Hindi" for Hindi/Hinglish questions
    """
    hindi_chars = sum(
        1 for char in text
        if "\u0900" <= char <= "\u097F"
    )

    if hindi_chars > 0:
        return "Hindi"

    return "English"

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
        language = detect_language(prompt)

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
                        f"The user's question is in {language}. "
                        f"You MUST answer entirely in {language}. "
                        "Do not switch to another language. "
                        "Do not mix languages."
                    ),
                },
                {
                    "role": "user",
                    "content": f"""
user: {prompt}

video_context: {chunk_list}
""",
                },
            ],
        )

        return response.choices[0].message.content

    except Exception as e:
        raise Exception(f"error: {e}")