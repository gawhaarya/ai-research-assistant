import pytest
from unittest.mock import Mock
from agent import execute_tool
from agent import run_research

def test_agent_rejects_empty_question():
    with pytest.raises(ValueError, match="cannot be empty"):
        run_research("   ")

@pytest.mark.integration
def test_agent_returns_structured_report():
    report = run_research(
        "What is RAG, and what are its limitations?"
    )

    assert report.question
    assert report.summary
    assert len(report.key_findings) >= 1
    assert isinstance(report.sources_used, list)
    assert isinstance(report.tools_used, list)

@pytest.mark.integration
def test_agent_reports_unknown_topic_without_inventing_a_source():
    report = run_research(
        "Explain quantum computing based on the available research notes."
    )

    assert report.question
    assert report.summary
    assert "quantum-computing" not in report.sources_used
    
def test_unknown_tool_is_rejected():
    with pytest.raises(ValueError, match="Tool is not allowed"):
        execute_tool("delete_all_files", {})


def test_malformed_tool_arguments_are_rejected():
    with pytest.raises(ValueError, match="Expected one string argument"):
        execute_tool("search_research_notes", {"wrong_argument": "RAG"})


def test_tool_failure_is_propagated(monkeypatch):
    def failing_search(query):
        raise ValueError("Simulated tool failure")

    monkeypatch.setitem(
        __import__("agent").TOOL_REGISTRY,
        "search_research_notes",
        failing_search,
    )

    with pytest.raises(ValueError, match="Simulated tool failure"):
        execute_tool("search_research_notes", {"query": "RAG"})