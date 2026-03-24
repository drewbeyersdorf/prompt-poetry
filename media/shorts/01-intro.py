#!/usr/bin/env python3
"""YouTube Short #1: What is prompt-poetry? (45 seconds)

This script generates the terminal output that gets screen-recorded.
Run it, screen record with OBS, crop to 9:16, done.

Or: asciinema rec --command "python media/shorts/01-intro.py" intro.cast
Then: agg intro.cast intro.gif --cols 60 --rows 30
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
section("What if prompt engineering was composable?")
pause(1.5)

print()
slow_print("\033[90m# Without prompt-poetry:\033[0m")
pause(0.5)
slow_print('\033[37m"Why did costs increase?"\033[0m')
pause(0.8)
slow_print("\033[90m# Vague question. Vague answer.\033[0m")
pause(1.5)

print()
section("With prompt-poetry:")
pause(0.5)

slow_print("\033[33mfrom\033[0m prompt_poetry.presets \033[33mimport\033[0m analyst")
pause(0.3)
print()
slow_print('\033[37manalyst(\033[32m"Why did costs increase?"\033[37m)\033[0m')
pause(1.0)

print()
slow_print("\033[90m# Output:\033[0m")
pause(0.3)
print()

# Simulate the actual output
from prompt_poetry.presets import analyst
result = analyst("Why did costs increase?")
for line in result.split("\n"):
    slow_print(f"\033[36m{line}\033[0m", delay=0.015)
    time.sleep(0.1)

pause(1.5)
print()
section("8 techniques. One pipe operator. Zero deps.")
pause(0.5)
slow_print("\033[90mgithub.com/drewbeyersdorf/prompt-poetry\033[0m")
pause(2.0)
