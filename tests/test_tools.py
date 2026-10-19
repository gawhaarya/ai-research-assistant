import pytest

from tools.research_tools import (
    search_research_notes,
    get_research_note,
)


def test_search_finds_rag():
    result = search_research_notes("RAG")

    assert result["count"] >= 1
    assert result["results"][0]["id"] == "rag"


def test_search_returns_empty_for_unknown_topic():
    result = search_research_notes("quantum computing")

    assert result["count"] == 0
    assert result["results"] == []


def test_search_rejects_empty_query():
    with pytest.raises(ValueError):
        search_research_notes("   ")


def test_get_research_note_returns_full_note():
    note = get_research_note("rag")

    assert note["id"] == "rag"
    assert "content" in note
    assert len(note["content"]) > 0


def test_get_research_note_rejects_unknown_id():
    with pytest.raises(ValueError):
        get_research_note("unknown-topic")