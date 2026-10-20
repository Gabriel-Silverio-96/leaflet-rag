from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
VECTOR_STORE_DIR = PROJECT_ROOT / "vector_store"


@dataclass(frozen=True)
class LeafletConfig:
    name: str
    aliases: tuple[str, ...]
    pdf_path: Path
    vector_store_path: Path


LEAFLETS = {
    "dipyrone": LeafletConfig(
        name="Dipyrone",
        aliases=("dipyrone", "dipirona", "dipirona monoidratada"),
        pdf_path=DATA_DIR / "dipirona" / "dipirona.pdf",
        vector_store_path=VECTOR_STORE_DIR / "dipirona.json",
    ),
    "hydrochlorothiazide": LeafletConfig(
        name="Hydrochlorothiazide",
        aliases=("hydrochlorothiazide", "hidroclorotiazida"),
        pdf_path=DATA_DIR / "hidroclorotiazida" / "hidroclorotiazida.pdf",
        vector_store_path=VECTOR_STORE_DIR / "hidroclorotiazida.json",
    ),
    "losartan-potassium": LeafletConfig(
        name="Losartan potassium",
        aliases=(
            "losartan",
            "losartan potassium",
            "losartana",
            "losartana potassica",
        ),
        pdf_path=DATA_DIR / "losartana-potassio" / "losartana.pdf",
        vector_store_path=VECTOR_STORE_DIR / "losartana-potassio.json",
    ),
}

EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
RETRIEVER_K = 5
CHAT_MODEL_NAME = "gemini-3.5-flash-lite"
