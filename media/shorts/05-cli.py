#!/usr/bin/env python3
"""YouTube Short #5: CLI Demo (30 seconds)

Shows the command-line tool.
"""

import time
import sys
import subprocess


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


def run_cmd(cmd):
    """Type the command slowly, then show real output."""
    slow_print(f"\033[32m$ {cmd}\033[0m", delay=0.04)
    pause(0.3)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    for line in result.stdout.strip().split("\n")[:6]:
        slow_print(f"\033[37m{line}\033[0m", delay=0.015)
    pause(1.0)


# --- Script ---

print()
section("prompt-poetry has a CLI.")
pause(1.0)

run_cmd('prompt-poetry --preset analyst "Why is churn increasing?"')

print()
run_cmd('prompt-poetry --persona "forensic accountant" --prime urgency "Review Q4 invoices"')

print()
run_cmd('prompt-poetry --list-presets')

pause(1.0)
print()
section("Enhance prompts from your terminal.")
slow_print("\033[90mpip install git+https://github.com/drewbeyersdorf/prompt-poetry\033[0m")
pause(2.0)
