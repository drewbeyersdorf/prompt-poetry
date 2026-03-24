"""Example: anti-hallucination RAG pipeline.

Wrap your RAG system prompt with precision priming and a constitution
to measurably reduce fabrication in retrieval-augmented generation.
"""

from prompt_poetry import prime, constrain, ritual, constitution

# Build a RAG-specific pipeline
rag_system = (
    constitution(
        role="knowledge assistant",
        rules=[
            "ONLY use information from the provided context — never invent facts",
            "If context is insufficient, say so rather than guessing",
            "Cite every claim with [N] references",
            "Never attribute quotes to people unless the source explicitly says so",
        ],
        values=[
            "Precision over completeness",
            "Evidence over assertion",
        ],
    )
    | prime("precision")
    | ritual("show reasoning")
    | constrain("cite sources with [N]", "state confidence level for each claim")
)


def build_rag_prompt(question: str, context_chunks: list[str]) -> str:
    """Build a complete RAG prompt with anti-hallucination techniques."""
    context = "\n\n".join(
        f"[{i+1}] {chunk}" for i, chunk in enumerate(context_chunks)
    )
    return rag_system(f"Question: {question}\n\nContext:\n{context}")


if __name__ == "__main__":
    chunks = [
        "Q3 revenue was $6.2M, up 12% from Q2.",
        "The engineering team grew from 8 to 14 people in Q3.",
        "Customer NPS dropped from 72 to 65 after the pricing change.",
    ]

    prompt = build_rag_prompt("What happened in Q3?", chunks)
    print(prompt)
    print(f"\n{'─' * 60}")
    print(f"Prompt length: {len(prompt)} chars")
    print(f"Techniques applied: constitution + precision + reasoning + constraints")
