import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import IO, Any, Literal

from services.query import user_query
from services.ollama_connection import llama3_model
from services.chunk_extractor import chunk_extractor
from services.embadding import _chromadb_text_to_vector

class userURL(BaseModel):
    url: str
class userQuery(BaseModel):
    query: str
    video_id: str

app = FastAPI(
    title="TubeTalk RAG Api",
    description="""
    This api use for ask query any youtube video from your chat box not need to watch full video.
    """,
    version="1.0.0"
)


@app.get("/")
async def home():
    return {"message": "welcome TubeTalk API"}


@app.post("/yourube_url")
async def text_extractor(data: userURL):
    try:
        result = chunk_extractor(data.url)
        res = _chromadb_text_to_vector(result["text"], result["video_id"])
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
async def ask_query(query: userQuery):
    try:
        result = user_query(query.query, query.video_id)
        ai_responce = llama3_model(query.query, result[0])
        return {"message": str(ai_responce)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))