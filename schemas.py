from pydantic import BaseModel, Field

class ResearchReport(BaseModel):
    question: str = Field(
        min_length=1,
        description="The user's original research question.",
    )

    summary: str = Field(
        min_length=1,
        description="A concise answer to the research question.",
    )

    key_findings: list[str] = Field(
        min_length=1,
        description="Important findings supporting the summary.",
    )

    sources_used: list[str] = Field(
        default_factory=list,
        description="IDs or names of sources used.",
    )

    tools_used: list[str] = Field(
        default_factory=list,
        description="Tools executed during research.",
    )