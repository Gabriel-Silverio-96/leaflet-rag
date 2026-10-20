import json

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

from leaflet_rag.config import CHUNK_OVERLAP, CHUNK_SIZE, LEAFLETS


def load_or_build_vector_store(
    leaflet_id: str,
    embedding_model,
    *,
    rebuild: bool = False,
) -> InMemoryVectorStore:
    leaflet = LEAFLETS[leaflet_id]
    vector_store_path = leaflet.vector_store_path

    if vector_store_path.exists() and not rebuild:
        print(f"Vector store loaded: {vector_store_path}")
        return InMemoryVectorStore.load(str(vector_store_path), embedding_model)

    metadata_path = leaflet.pdf_path.parent / "metadata.json"
    with metadata_path.open("r", encoding="utf-8") as metadata_file:
        leaflet_metadata = json.load(metadata_file)

    documents = PyPDFLoader(str(leaflet.pdf_path)).load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(documents)

    for chunk in chunks:
        chunk.metadata.update(leaflet_metadata)
        chunk.metadata["title"] = leaflet_metadata["medicationName"]

    vector_store_path.parent.mkdir(parents=True, exist_ok=True)
    vector_store = InMemoryVectorStore(embedding_model)
    vector_store.add_documents(chunks)
    vector_store.dump(str(vector_store_path))

    print(f"Vector store created: {vector_store_path}")
    print(f"Indexed chunks: {len(chunks)}")
    return vector_store
