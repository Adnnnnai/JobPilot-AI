from .embedding import EmbeddingService
from .vector_store import get_collection
from .chunk import ResumeChunker


def index_resume(resume_json: dict, resume_id: int):
    chunks = ResumeChunker.from_json(resume_json)
    embeddings = EmbeddingService.embed(chunks)
    collection = get_collection("resumes")

    ids = [f"resume_{resume_id}_{i}" for i in range(len(chunks))]
    metadatas = [{"resume_id": resume_id} for _ in chunks]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas
    )


def search_resumes(query: str, n_results: int = 5):
    collection = get_collection("resumes")
    query_embedding = EmbeddingService.embed([query])

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )

    return results
