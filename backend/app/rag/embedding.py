import os

from sentence_transformers import SentenceTransformer

MODEL_PATH = os.path.join(
    os.path.expanduser("~"),
    ".cache",
    "modelscope",
    "models",
    "BAAI--bge-small-zh-v1.5",
    "snapshots",
    "master"
)


class EmbeddingService:

    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            cls._model = SentenceTransformer(MODEL_PATH)
        return cls._model

    @classmethod
    def embed(cls, texts: list[str]) -> list[list[float]]:
        model = cls.get_model()
        embeddings = model.encode(texts, normalize_embeddings=True)
        return embeddings.tolist()
