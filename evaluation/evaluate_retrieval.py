
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.research_tools import search_research_notes

CASES_FILE = PROJECT_ROOT / "evaluation" / "retrieval_cases.json"
K = 3


def load_evaluation_cases():
    """Load manually labelled retrieval test cases."""
    with CASES_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_case(case):
    """Evaluate one query against its expected relevant note IDs."""
    query = case["query"]
    expected_ids = set(case["expected_ids"])

    search_result = search_research_notes(query)
    retrieved_ids = [
        item["id"] for item in search_result["results"][:K]
    ]

    retrieved_set = set(retrieved_ids)
    relevant_retrieved = len(retrieved_set & expected_ids)

    if expected_ids:
        recall = relevant_retrieved / len(expected_ids)
    else:
        recall = None

    if retrieved_ids:
        precision = relevant_retrieved / len(retrieved_ids)
    else:
        precision = 1.0 if not expected_ids else 0.0

    if not expected_ids:
        passed = len(retrieved_ids) == 0
    else:
        passed = expected_ids.issubset(retrieved_set)

    return {
        "query": query,
        "expected_ids": sorted(expected_ids),
        "retrieved_ids": retrieved_ids,
        "recall_at_k": recall,
        "precision_at_k": precision,
        "passed": passed,
    }


def main():
    cases = load_evaluation_cases()
    results = [evaluate_case(case) for case in cases]

    print(f"Retrieval Evaluation (k={K})")
    print("=" * 50)

    for result in results:
        status = "PASS" if result["passed"] else "FAIL"
        print(f"\n[{status}] {result['query']}")
        print(f"  Expected:  {result['expected_ids']}")
        print(f"  Retrieved: {result['retrieved_ids']}")
        print(f"  Recall@{K}:    {result['recall_at_k']}")
        print(f"  Precision@{K}: {result['precision_at_k']}")

    passed_count = sum(result["passed"] for result in results)
    print("\n" + "=" * 50)
    print(f"Passed: {passed_count}/{len(results)}")

    measured_recalls = [
        result["recall_at_k"]
        for result in results
        if result["recall_at_k"] is not None
    ]

    if measured_recalls:
        mean_recall = sum(measured_recalls) / len(measured_recalls)
        print(f"Mean Recall@{K}: {mean_recall:.2f}")


if __name__ == "__main__":
    main()