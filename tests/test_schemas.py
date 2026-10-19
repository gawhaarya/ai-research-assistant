import pytest
from pydantic import ValidationError

from schemas import ResearchReport


def test_valid_research_report():
    report = ResearchReport(
        question="What is RAG?",
        summary="RAG grounds answers using retrieved information.",
        key_findings=["It retrieves relevant context."],
        sources_used=["rag"],
        tools_used=["search_research_notes", "get_research_note"],
    )

    assert report.question == "What is RAG?"
    assert len(report.key_findings) == 1


def test_empty_summary_is_rejected():
    with pytest.raises(ValidationError):
        ResearchReport(
            question="What is RAG?",
            summary="",
            key_findings=["It retrieves relevant context."],
        )