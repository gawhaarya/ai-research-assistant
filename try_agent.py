from agent import run_research

report = run_research(
    "What is Retrieval-Augmented Generation, and how does it help reduce hallucinations?"
)

print(report.model_dump_json(indent=2))