# AI Research Assistant

A tool-using research assistant built with Python, Google's Gemini API, Pydantic, and Streamlit. It searches a small local research knowledge base and produces structured research reports.

## Features

- **Tool calling:** The LLM can request approved research tools.
- **Local knowledge retrieval:** Search research notes and retrieve complete notes by ID.
- **Structured output:** Pydantic validates the research report's structure.
- **Input validation:** Rejects empty questions and malformed tool arguments.
- **Tool safety:** Only explicitly registered tools can execute.
- **Error handling:** Provides readable messages for API and tool failures.
- **Evaluation:** Includes a small labelled retrieval dataset with Recall@k and Precision@k metrics.
- **Automated tests:** Covers tools, schema validation, agent safety and retrieval evaluation.

## Architecture

1. The user submits a question through the Streamlit interface.
2. The agent sends the question to Gemini with approved tool definitions.
3. Gemini can request a local research tool.
4. The application validates and executes the requested tool.
5. The tool result is returned to Gemini for further reasoning.
6. The agent validates the final report using Pydantic.
7. Streamlit displays the summary, key findings, sources and tools used.

## Technology Stack

- Python
- Google Gemini API
- Google Gen AI SDK
- Streamlit
- Pydantic
- pytest

## Project Structure

```text
AI Research Assistant/
├── app.py
├── agent.py
├── config.py
├── schemas.py
├── tools/
│   └── research_tools.py
├── data/
│   └── research_notes.json
├── evaluation/
│   ├── retrieval_cases.json
│   └── evaluate_retrieval.py
├── tests/
├── .env
├── .gitignore
└── pyproject.toml
```

## Setup

1. Create and activate a Python virtual environment.
2. Install the project's dependencies.
3. Create a `.env` file with a Gemini API key:

   `GEMINI_API_KEY=your_api_key_here`

4. Start the application:

   `python -m streamlit run app.py`

## Run Tests

Run the local test suite:

`python -m pytest tests -v`

Tests marked as integration tests are excluded by default to avoid unnecessary live API calls.

Run retrieval evaluation separately:

`python evaluation/evaluate_retrieval.py`

## Current Limitations

- Research is limited to the local notes in `data/research_notes.json`.
- Retrieval uses simple keyword matching rather than semantic embeddings.
- The evaluation dataset is small and manually labelled.
- The quality of generated reports depends on the LLM, retrieved context and API availability.
- This project does not currently perform live internet searches.

## Security

- Keep API keys in environment variables; never commit `.env`.
- Validate tool names and arguments before execution.
- Do not allow model-generated text to execute arbitrary code or shell commands.
- Treat retrieved content as untrusted input.

## Future Improvements

- Add an approved web-search tool.
- Improve retrieval with embeddings and a vector database.
- Expand the evaluation dataset and add answer-quality evaluation.
- Add citations linking findings to specific source passages.
- Improve logging and observability.