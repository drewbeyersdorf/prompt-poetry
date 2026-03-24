#!/usr/bin/env python3
"""YouTube Short #4: 12 Presets (45 seconds)

Shows presets for different roles.
"""

import time
import sys


def slow_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def pause(seconds=1.0):
    time.sleep(seconds)


def section(text):
    print(f"\033[1;36m{text}\033[0m")
    pause(0.5)


# --- Script ---

print()
section("12 presets. Every role covered.")
pause(1.5)

from prompt_poetry.presets import analyst, debugger, briefer, customer_responder, rag_strict

demos = [
    ("analyst",    analyst,             "Why did margins drop 3%?"),
    ("debugger",   debugger,            "CI fails but tests pass locally"),
    ("briefer",    briefer,             "Update on the warehouse expansion"),
    ("customer",   customer_responder,  "Order arrived damaged, wants refund"),
    ("rag_strict", rag_strict,          "What was revenue last quarter?"),
]

for name, preset, question in demos:
    print()
    slow_print(f"\033[33m{name}\033[37m(\033[32m\"{question}\"\033[37m)\033[0m")
    pause(0.3)
    result = preset(question)
    first_line = result.strip().split("\n")[0][:65]
    slow_print(f"  \033[36m-> {first_line}...\033[0m", delay=0.02)
    pause(0.8)

pause(1.0)
print()
section("One import. One line. Better prompts.")
pause(0.5)
slow_print("\033[90mgithub.com/drewbeyersdorf/prompt-poetry\033[0m")
pause(2.0)
