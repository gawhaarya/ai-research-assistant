import json
from pathlib import Path
from typing import Any

# Find the project root and the research notes file.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
NOTES_FILE = PROJECT_ROOT / "data" / "research_notes.json"

def load_research_notes() -> list[dict[str, Any]]:
    """Load research notes from the local JSON file."""
    with NOTES_FILE.open("r", encoding="utf-8") as file:
        notes = json.load(file)

    if not isinstance(notes, list):
        raise ValueError("Research notes must be a JSON list.")

    return notes

def search_research_notes(query: str) -> dict[str, Any]:
    """Search research notes using a simple keyword-matching approach."""
    query = query.strip().lower()

    if not query:
        raise ValueError("Search query cannot be empty.")

    notes = load_research_notes()
    query_words = set(query.split())
    results = []

    for note in notes:
        searchable_text = " ".join(
            [note["title"], note["id"], *note["keywords"]]
        ).lower()

        matching_words = query_words.intersection(
            set(searchable_text.split())
        )

        if matching_words:
            results.append({
                "id": note["id"],
                "title": note["title"],
                "matched_terms": sorted(matching_words),
                "content_preview": note["content"][:180],
            })

    return {
        "query": query,
        "results": results,
        "count": len(results),
    }


def get_research_note(note_id: str) -> dict[str, Any]:
    """Retrieve the full research note using its ID."""
    note_id = note_id.strip().lower()

    if not note_id:
        raise ValueError("Note ID cannot be empty.")

    notes = load_research_notes()

    for note in notes:
        if note["id"] == note_id:
            return note

    raise ValueError(f"No research note found for ID: {note_id}")