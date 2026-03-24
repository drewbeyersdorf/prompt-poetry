"""Command-line interface for prompt-poetry.

Usage:
    prompt-poetry "your prompt here"
    prompt-poetry --preset analyst "What's driving costs?"
    prompt-poetry --persona "forensic accountant" --prime urgency "Review these invoices"
    prompt-poetry --list-presets
    prompt-poetry --list-techniques
    echo "your prompt" | prompt-poetry --preset debugger
"""

from __future__ import annotations

import argparse
import sys

from prompt_poetry import (
    persona, prime, constrain, ritual, meta, narrative, toggle, constitution,
    __version__,
)
from prompt_poetry.presets import analyst, debugger, researcher, evaluator, writer

_PRESETS = {
    "analyst": analyst,
    "debugger": debugger,
    "researcher": researcher,
    "evaluator": evaluator,
    "writer": writer,
}

_TECHNIQUES_HELP = """
The 8 Techniques:

  1. persona     Identity injection          --persona "master craftsman"
  2. prime       Emotional temperature        --prime urgency
  3. constrain   Tighter bounds, better out   --constrain "under 100 words"
  4. ritual      Chain-of-thought ceremony    --ritual "step by step"
  5. meta        Prompt improves itself       --meta
  6. narrative   Story as structure           --narrative postmortem
  7. toggle      Binary behavioral knobs      --toggle depth=deep,creativity=high
  8. constitution Persistent identity         --constitution role=auditor
"""


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="prompt-poetry",
        description="Composable prompt engineering. Every word is a probability lever.",
    )
    parser.add_argument("prompt", nargs="?", help="The prompt to enhance (or pipe via stdin)")
    parser.add_argument("--version", action="version", version=f"prompt-poetry {__version__}")
    parser.add_argument("--preset", "-p", choices=_PRESETS.keys(), help="Apply a preset pipeline")
    parser.add_argument("--persona", help="Set persona identity")
    parser.add_argument("--prime", help="Set emotional primer (urgency, precision, creativity, calm, confidence)")
    parser.add_argument("--constrain", "-c", help="Add constraints (comma-separated)")
    parser.add_argument("--ritual", help="Set thinking ritual")
    parser.add_argument("--meta", action="store_true", help="Enable meta-prompt self-improvement")
    parser.add_argument("--narrative", help="Set narrative style (case study, scene, parable, briefing, postmortem)")
    parser.add_argument("--toggle", "-t", help="Set toggles as key=value pairs (comma-separated)")
    parser.add_argument("--list-presets", action="store_true", help="List available presets")
    parser.add_argument("--list-techniques", action="store_true", help="List all techniques")

    args = parser.parse_args(argv)

    if args.list_presets:
        print("Available presets:\n")
        print("  analyst     Commits to answers, cites numbers, goes deep")
        print("  debugger    Step-by-step, root cause, precise")
        print("  researcher  Case study framing, creative, thorough")
        print("  evaluator   Scoring ritual, no hedging")
        print("  writer      Casual voice, bold, no jargon")
        return

    if args.list_techniques:
        print(_TECHNIQUES_HELP.strip())
        return

    # Get prompt from args or stdin
    prompt_text = args.prompt
    if not prompt_text and not sys.stdin.isatty():
        prompt_text = sys.stdin.read().strip()
    if not prompt_text:
        parser.print_help()
        sys.exit(1)

    # Build the pipeline
    if args.preset:
        pipeline = _PRESETS[args.preset]
    else:
        transforms = []
        if args.persona:
            transforms.append(persona(args.persona))
        if args.prime:
            transforms.append(prime(args.prime))
        if args.ritual:
            transforms.append(ritual(args.ritual))
        if args.meta:
            transforms.append(meta())
        if args.narrative:
            transforms.append(narrative(args.narrative))
        if args.toggle:
            pairs = dict(kv.split("=") for kv in args.toggle.split(","))
            transforms.append(toggle(**pairs))
        if args.constrain:
            parts = [c.strip() for c in args.constrain.split(",")]
            transforms.append(constrain(*parts))

        if not transforms:
            # No techniques specified - just echo the prompt
            print(prompt_text)
            return

        # Chain them
        pipeline = transforms[0]
        for t in transforms[1:]:
            pipeline = pipeline | t

    print(pipeline(prompt_text))


if __name__ == "__main__":
    main()
