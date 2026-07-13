from ..embedding import EmbeddingService
from ..vector_store import get_collection


class InterviewKB:

    COLLECTION = "interview_questions"

    @staticmethod
    def index(question: str, answer: str, tags: list[str] = None):
        doc = f"Q: {question}\nA: {answer}"
        chunks = [doc]
        embeddings = EmbeddingService.embed(chunks)
        collection = get_collection(InterviewKB.COLLECTION)

        qid = str(hash(question) % 10**8)
        collection.upsert(
            ids=[f"iq_{qid}"],
            embeddings=embeddings,
            documents=chunks,
            metadatas=[{
                "question": question,
                "tags": ",".join(tags) if tags else ""
            }]
        )

    @staticmethod
    def search(query: str, n_results: int = 5):
        collection = get_collection(InterviewKB.COLLECTION)
        query_embedding = EmbeddingService.embed([query])
        return collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
