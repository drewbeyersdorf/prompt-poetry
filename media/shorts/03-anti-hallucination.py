#!/usr/bin/env python3
"""YouTube Short #3: Anti-Hallucination RAG (45 seconds)

Shows the constitution technique reducing hallucination.
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
section("Your RAG system hallucinates.")
pause(1.0)
section("Here's the fix.")
pause(1.5)

print()
slow_print("\033[33mfrom\033[0m prompt_poetry \033[33mimport\033[0m constitution, prime")
pause(0.3)

print()
slow_print("\033[37mrag = constitution(\033[0m")
slow_print('\033[37m    role=\033[32m"knowledge assistant"\033[37m,\033[0m')
slow_print("\033[37m    rules=[\033[0m")
slow_print('\033[37m        \033[32m"ONLY use provided context"\033[37m,\033[0m')
slow_print('\033[37m        \033[32m"cite with [N] references"\033[37m,\033[0m')
slow_print('\033[37m        \033[32m"say I don\'t know if unsure"\033[37m,\033[0m')
slow_print("\033[37m    ]\033[0m")
slow_print("\033[37m) \033[35m|\033[37m prime(\033[32m\"precision\"\033[37m)\033[0m")
pause(1.0)

print()
slow_print("\033[90m# Every query gets these rules baked in:\033[0m")
pause(0.5)

print()
from prompt_poetry import constitution, prime
rag = constitution(
    role="knowledge assistant",
    rules=["ONLY use provided context", "cite with [N] references", "say I don't know if unsure"]
) | prime("precision")
result = rag("What was our Q3 revenue?")
for line in result.split("\n"):
    slow_print(f"\033[36m{line}\033[0m", delay=0.015)
    time.sleep(0.1)

pause(1.5)
print()
section("We cut hallucination from 8/13 to near zero.")
pause(1.0)
slow_print("\033[90mgithub.com/drewbeyersdorf/prompt-poetry\033[0m")
pause(2.0)
