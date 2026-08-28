import chromadb
from sentence_transformers import SentenceTransformer
from config import HF_TOKEN

model = SentenceTransformer('all-MiniLM-L6-v2')

def user_query(user_input: str, video_id: str):
    client = chromadb.PersistentClient(path="./chroma_db")
    try:
        try:
            collection = client.get_collection(video_id)
        except Exception:
            raise Exception(
                f"No processed data found for this video. Please process it again."
            )

        query_embeddings = model.encode(user_input).tolist()
        results = collection.query(
            query_embeddings=[query_embeddings],
            n_results=3
        )
        context = results["documents"]
        return context

    except Exception as e:
        raise Exception(f"error: {e}")