#!/usr/bin/env python3
"""Enhance fine-tuning training data with prompt-poetry techniques.

Takes existing JSONL training pairs and enhances the system prompt with
precision priming, anti-hallucination constitution, and reasoning rituals.
Also enhances user prompts to trigger better assistant responses.

This is Phase 3 of prompt-poetry: the model learns to behave as if it's
been prompt-poetry'd even without the techniques applied at inference time.

Usage:
    python enhance_training_data.py input.jsonl output.jsonl [--format anthropic|openai|google]
"""

import json
import sys
from pathlib import Path

# Add prompt-poetry to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from prompt_poetry import prime, constrain, ritual, constitution

# Enhancement applied to every system prompt
SYSTEM_ENHANCEMENT = constitution(
    role="Methodology's institutional knowledge assistant — a precision instrument for company intelligence",
    rules=[
        "ONLY use information you have internalized from the documentary record — never invent facts",
        "If you don't have enough information to answer accurately, say so rather than guessing",
        "Never attribute statements, roles, or decisions to people unless you are certain from the record",
        "Include specific dates, names, and numbers when available",
        "When uncertain about a detail, state your confidence level",
    ],
    values=[
        "Precision over completeness — a correct partial answer beats a hallucinated full answer",
        "Evidence over assertion — cite what you know and where you know it from",
    ],
)

SYSTEM_PREFIX = (
    "Be meticulous and exact. Double-check every claim. "
    "Rigorous accuracy is non-negotiable.\n\n"
)

# Enhancement applied to user prompts (subtle — just adds precision framing)
USER_ENHANCEMENT = prime("precision")


def enhance_anthropic(line: dict) -> dict:
    """Enhance an Anthropic-format training pair."""
    messages = line.get("messages", [])
    enhanced = []

    for msg in messages:
        role = msg.get("role", "")
        content = msg.get("content", "")

        if role == "system":
            # Prepend precision priming + append constitution rules
            enhanced_content = SYSTEM_PREFIX + content
            # Add anti-hallucination footer if not already present
            if "never invent" not in content.lower():
                constitution_text = SYSTEM_ENHANCEMENT("")
                enhanced_content += "\n\n" + constitution_text
            enhanced.append({"role": role, "content": enhanced_content})
        elif role == "user":
            enhanced.append({"role": role, "content": content})
        else:
            # assistant responses stay unchanged — they're the ground truth
            enhanced.append(msg)

    return {"messages": enhanced}


def enhance_qa(line: dict) -> dict:
    """Enhance a QA-pair format (question/answer)."""
    question = line.get("question", "")
    answer = line.get("answer", "")

    # Keep the answer unchanged — it's ground truth
    # Enhance the question with precision framing
    enhanced_q = USER_ENHANCEMENT(question)

    result = dict(line)
    result["question"] = enhanced_q
    result["enhanced"] = True
    return result


def detect_format(first_line: dict) -> str:
    """Detect training data format from first line."""
    if "messages" in first_line:
        return "anthropic"
    if "question" in first_line and "answer" in first_line:
        return "qa"
    return "unknown"


def main():
    if len(sys.argv) < 3:
        print("Usage: enhance_training_data.py input.jsonl output.jsonl")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not input_path.exists():
        print(f"Error: {input_path} not found")
        sys.exit(1)

    # Read all lines
    lines = []
    with open(input_path) as f:
        for line in f:
            line = line.strip()
            if line:
                lines.append(json.loads(line))

    if not lines:
        print("Error: empty input file")
        sys.exit(1)

    # Detect format
    fmt = detect_format(lines[0])
    print(f"Detected format: {fmt}")
    print(f"Input: {len(lines)} pairs")

    # Enhance
    enhanced = []
    for line in lines:
        if fmt == "anthropic":
            enhanced.append(enhance_anthropic(line))
        elif fmt == "qa":
            enhanced.append(enhance_qa(line))
        else:
            print(f"Warning: unknown format, passing through unchanged")
            enhanced.append(line)

    # Write output
    with open(output_path, "w") as f:
        for line in enhanced:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")

    print(f"Output: {len(enhanced)} enhanced pairs → {output_path}")

    # Show a sample
    sample = enhanced[0]
    if fmt == "anthropic":
        sys.msg = sample["messages"][0]
        print(f"\nSample system prompt (first 200 chars):")
        print(f"  {sys.msg['content'][:200]}...")
    elif fmt == "qa":
        print(f"\nSample enhanced question:")
        print(f"  {sample['question'][:200]}...")


if __name__ == "__main__":
    main()
