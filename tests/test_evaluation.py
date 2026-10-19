from evaluation.evaluate_retrieval import evaluate_case

def test_rag_query_retrieves_expected_note():
    result = evaluate_case({
        "query": "RAG hallucination",
        "expected_ids": ["rag"],
    })

    assert result["passed"] is True
    assert result["recall_at_k"] == 1.0


def test_unknown_topic_returns_no_results():
    result = evaluate_case({
        "query": "quantum computing",
        "expected_ids": [],
    })

    assert result["passed"] is True
    assert result["retrieved_ids"] == []
    assert result["recall_at_k"] is None


def test_unretrieved_expected_note_fails(monkeypatch):
    def fake_search(query):
        return {
            "query": query,
            "results": [],
            "count": 0,
        }

    monkeypatch.setattr(
        "evaluation.evaluate_retrieval.search_research_notes",
        fake_search,
    )

    result = evaluate_case({
        "query": "RAG hallucination",
        "expected_ids": ["rag"],
    })

    assert result["passed"] is False
    assert result["recall_at_k"] == 0.0