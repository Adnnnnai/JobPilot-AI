from ..embedding import EmbeddingService
from ..vector_store import get_collection
from ..chunk import ResumeChunker


class ResumeKB:

    COLLECTION = "resumes"

    @staticmethod
    def index(resume_json: dict, resume_id: int):
        chunks = ResumeChunker.from_json(resume_json)
        embeddings = EmbeddingService.embed(chunks)
        collection = get_collection(ResumeKB.COLLECTION)

        ids = [f"resume_{resume_id}_{i}" for i in range(len(chunks))]
        metadatas = [{"resume_id": resume_id} for _ in chunks]

        collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas
        )

    @staticmethod
    def search(query: str, n_results: int = 5):
        collection = get_collection(ResumeKB.COLLECTION)
        query_embedding = EmbeddingService.embed([query])
        return collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
