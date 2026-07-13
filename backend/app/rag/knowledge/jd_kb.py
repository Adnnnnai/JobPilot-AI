from ..embedding import EmbeddingService
from ..vector_store import get_collection


class JDKB:

    COLLECTION = "job_descriptions"

    @staticmethod
    def index(jd_text: str, jd_id: str):
        chunks = [jd_text]
        embeddings = EmbeddingService.embed(chunks)
        collection = get_collection(JDKB.COLLECTION)

        collection.upsert(
            ids=[f"jd_{jd_id}"],
            embeddings=embeddings,
            documents=chunks,
            metadatas=[{"jd_id": jd_id}]
        )

    @staticmethod
    def search(query: str, n_results: int = 5):
        collection = get_collection(JDKB.COLLECTION)
        query_embedding = EmbeddingService.embed([query])
        return collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
