import re
import unicodedata

from leaflet_rag.config import LEAFLETS


def normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text.lower().replace("-", " "))
    without_accents = "".join(
        character
        for character in normalized
        if not unicodedata.combining(character)
    )
    return re.sub(r"[^a-z0-9]+", " ", without_accents).strip()


def detect_leaflet(query: str) -> str | None:
    normalized_query = f" {normalize_text(query)} "
    matches = []

    for leaflet_id, leaflet in LEAFLETS.items():
        for alias in leaflet.aliases:
            normalized_alias = normalize_text(alias)
            if f" {normalized_alias} " in normalized_query:
                matches.append(leaflet_id)
                break

    if len(matches) == 1:
        return matches[0]

    return None
