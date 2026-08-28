import os
from dotenv import load_dotenv

from langfuse.openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama',
)

def llama3_model(prompt: str, chunk_list: list):

    try:
        response = client.chat.completions.create(
            model="llama3.2",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant named Tube AI. This is a RAG-based system "
                        "that summarizes YouTube videos and answers user queries about them. "
                        "We internally pass you a text chunk from the video relevant to the user's query. "
                        "Using this chunk, you must answer the user's question directly and naturally, "
                        "without mentioning that you were given a 'chunk' or referencing anything not "
                        "visible in the chat. Make sure the user is fully satisfied with your answer.\n\n"
                        "IMPORTANT LANGUAGE RULE: Always respond in the SAME language the user used to "
                        "ask their question, regardless of what language the video_chunk is in. "
                        "For example, if the user asks in English but the video_chunk is in Hindi, "
                        "translate the relevant information and answer in English. "
                        "If the user asks in Hindi, answer in Hindi. Never mirror the chunk's language "
                        "over the user's question language."
                    )
                },
                {
                    "role": "user",
                    "content": f"""
                    user: {prompt}
                    video_chunk: {chunk_list}
                    """
                }
            ]
        )
        print(chunk_list)
        msg = response.choices[0].message.content
        return msg

    except Exception as e:
        raise Exception(f"error: {e}")