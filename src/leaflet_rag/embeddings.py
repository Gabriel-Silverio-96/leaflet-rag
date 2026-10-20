from langchain_huggingface import HuggingFaceEmbeddings

from leaflet_rag.config import EMBEDDING_MODEL_NAME


def create_embedding_model() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
