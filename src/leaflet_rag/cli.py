import argparse

from dotenv import load_dotenv

from leaflet_rag.config import LEAFLETS
from leaflet_rag.embeddings import create_embedding_model
from leaflet_rag.indexing import load_or_build_vector_store
from leaflet_rag.rag import answer_question
from leaflet_rag.routing import detect_leaflet
from leaflet_rag.welcome import welcome

def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(description="Query medication leaflets with RAG")
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="rebuild the selected leaflet index",
    )
    parser.add_argument(
        "--index-only",
        action="store_true",
        help="create/load all leaflet indexes and exit",
    )
    args = parser.parse_args()

    if args.index_only:
        embedding_model = create_embedding_model()
        for leaflet_id in LEAFLETS:
            load_or_build_vector_store(
                leaflet_id,
                embedding_model,
                rebuild=args.rebuild,
            )
        return
    
    welcome()
    query = input("Enter your question about a medication: ").strip()
    
    leaflet_id = detect_leaflet(query)

    if leaflet_id is None:
        medication_names = ", ".join(
            leaflet.name for leaflet in LEAFLETS.values()
        )
        print(
            "Could not identify exactly one medication in the question. "
            f"Please specify one of these: {medication_names}."
        )
        return

    leaflet = LEAFLETS[leaflet_id]
    print(f"Selected leaflet: {leaflet.name}")

    try:
        embedding_model = create_embedding_model()
        vector_store = load_or_build_vector_store(
            leaflet_id,
            embedding_model,
            rebuild=args.rebuild,
        )
        answer = answer_question(query, leaflet.name, vector_store)

        print("\n=== RAG ANSWER ===")
        print(answer)
    except Exception as error:
        print("\n=== ERROR ===")
        print("Type:", type(error).__name__)
        print("Details:", error)
