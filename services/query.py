import chromadb
from sentence_transformers import SentenceTransformer

from config import HF_TOKEN

#load embadding model
model = SentenceTransformer('all-MiniLM-L6-v2')



def user_query(user_niput: str, video_id:str):
    #connect to local DB
    client =chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(video_id)

    try:

        query_embaddings = model.encode(user_niput).tolist()

        results = collection.query(
        query_embeddings=[query_embaddings],
        n_results=3
        )
        context = results["documents"]

        return context
    
    except Exception as e:
        raise Exception(f"error{e}")


