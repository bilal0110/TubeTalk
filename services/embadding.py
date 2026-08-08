import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai


import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer

from config import GOOGLE_API_KEY
from config import HF_TOKEN

# chromaDB model configer
model = SentenceTransformer("all-MiniLM-L6-v2") 


def _gemini_text_to_vector(document: str):

    """ this function user for conver long text into small chunks and srote them to a vector database"""
    # gemini embadding model configer
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    
    try:
        embaddings = []
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=0)
        chunks = text_splitter.split_text(document)
        for chunk in chunks:
            response = client.models.embed_content(
                model="gemini-embedding-001",
                contents=chunk
            )
            embaddings.append(response.embeddings[0].values)


    except Exception as e:
        print(f"Error:{e}")
        embaddings=[]

    return embaddings


def _chromadb_text_to_vector(document: str, video_id:str):
    print("Video_id", video_id)

  
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(
        name=f"{video_id}"
    )

    try:

        # generate chunks
        text_split = RecursiveCharacterTextSplitter(chunk_size = 200, chunk_overlap = 0)
        chunks = text_split.split_text(document)


        #generate embadding 
        embadding = model.encode(chunks).tolist()

        # generate ids
        ids = [f"{video_id}_chunk{i}" for i in range(len(chunks))]

        #metadata
        metadata = [{
            "video_id":video_id,
            "chunk_number": i
            }
            for i in range(len(chunks))
            ]

        # store data in chromaDB
        collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embadding,
            metadatas=metadata
            )
     

        return {"message": "✅ Data stored successfully!","video_id": video_id}
    except Exception as e:
        raise Exception(f"error: {e}")
       
    



       
     
