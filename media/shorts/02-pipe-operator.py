#!/usr/bin/env python3
"""YouTube Short #2: The Pipe Operator (45 seconds)

Shows how techniques compose with | like Unix pipes.
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
section("Unix has pipes. Now prompts do too.")
pause(1.5)

print()
slow_print("\033[33mfrom\033[0m prompt_poetry \033[33mimport\033[0m persona, prime, constrain")
pause(0.5)

print()
slow_print("\033[90m# Build a debugging pipeline:\033[0m")
pause(0.3)

print()
slow_print("\033[37mdebug = (\033[0m")
slow_print("\033[37m    persona(\033[32m\"principal SRE\"\033[37m)\033[0m")
slow_print("\033[37m    \033[35m|\033[37m prime(\033[32m\"precision\"\033[37m)\033[0m")
slow_print("\033[37m    \033[35m|\033[37m constrain(\033[32m\"root cause only\"\033[37m)\033[0m")
slow_print("\033[37m)\033[0m")
pause(1.0)

print()
slow_print("\033[90m# Use it:\033[0m")
slow_print('\033[37mdebug(\033[32m"API returning 500s on /users"\033[37m)\033[0m')
pause(1.0)

print()
from prompt_poetry import persona, prime, constrain
debug = persona("principal SRE") | prime("precision") | constrain("root cause only")
result = debug("API returning 500s on /users")
for line in result.split("\n"):
    slow_print(f"\033[36m{line}\033[0m", delay=0.015)
    time.sleep(0.1)

pause(1.5)
print()
section("Reusable. Testable. Composable.")
pause(0.5)
slow_print("\033[90mpip install git+https://github.com/drewbeyersdorf/prompt-poetry\033[0m")
pause(2.0)
