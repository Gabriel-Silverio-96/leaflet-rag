from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI

from leaflet_rag.config import CHAT_MODEL_NAME, RETRIEVER_K


def answer_question(
    query: str,
    medication_name: str,
    vector_store: InMemoryVectorStore,
) -> str:
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": RETRIEVER_K},
    )
    results = retriever.invoke(query)

    context = "\n\n".join(
        f"[Medication: {medication_name} | "
        f"page {result.metadata.get('page_label')}]\n"
        f"{result.page_content}"
        for result in results
    )

    prompt = f"""
Answer in English using only the leaflet excerpts below.
If they do not contain the answer, say that the information was not found
in the retrieved excerpts. Do not invent information.
Include the cited page numbers and medication name.

MEDICATION:
{medication_name}

LEAFLET EXCERPTS:
{context}

QUESTION:
{query}
"""

    model = ChatGoogleGenerativeAI(
        model=CHAT_MODEL_NAME,
        max_retries=1,
    )
    response = model.invoke(prompt)   

    return response.content[0]['text']

