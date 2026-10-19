import streamlit as st

from agent import run_research

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 AI Research Assistant")

st.write(
    "Ask a research question and get a structured report "
    "using AI tools and your research knowledge base."
)

st.info(
    "This version searches the local research notes you provide. "
    "It does not search the live internet."
)

with st.form("research_form"):
    question = st.text_area(
        "Your research question",
        placeholder=(
            "Example: What is RAG, and what are its limitations?"
        ),
        height=120,
    )

    submitted = st.form_submit_button(
        "Research",
        type="primary",
    )


if submitted:
    if not question.strip():
        st.warning("Please enter a research question.")
    else:
        try:
            with st.spinner("Researching your question..."):
                report = run_research(question)

            st.subheader("Research Summary")
            st.write(report.summary)

            st.subheader("Key Findings")
            for finding in report.key_findings:
                st.markdown(f"- {finding}")

            st.subheader("Sources Used")
            if report.sources_used:
                for source in report.sources_used:
                    st.markdown(f"- `{source}`")
            else:
                st.write("No sources were used.")

            st.subheader("Tools Used")
            if report.tools_used:
                for tool in report.tools_used:
                    st.markdown(f"- `{tool}`")
            else:
                st.write("No tools were used.")

        except (RuntimeError, ValueError) as exc:
            st.error(str(exc))

        except Exception:
            st.error(
                "Something unexpected went wrong. "
                "Check the terminal for details and try again."
            )