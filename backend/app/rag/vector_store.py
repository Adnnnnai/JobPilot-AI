import os

import chromadb
from chromadb.config import Settings


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
)

CHROMA_DIR = os.path.join(PROJECT_ROOT, "chroma_db")

_client = None


def get_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(
            path=CHROMA_DIR,
            settings=Settings(anonymized_telemetry=False)
        )
    return _client


def get_collection(name: str = "resumes"):
    client = get_client()
    return client.get_or_create_collection(
        name=name,
        metadata={"hnsw:space": "cosine"}
    )
