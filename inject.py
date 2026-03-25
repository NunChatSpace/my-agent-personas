#!/usr/bin/env python3
"""
inject.py — Injects persona content into a target file using markers.

Usage:
    python3 inject.py <persona_file> <target_file>

Behavior:
    - If target has markers: replaces content between them
    - If target exists but no markers: prepends persona block
    - If target doesn't exist: creates it with persona block
"""

import sys
import os

START_MARKER = "<!-- PERSONA:START -->"
END_MARKER = "<!-- PERSONA:END -->"


def inject(persona_file: str, target_file: str) -> None:
    with open(persona_file, "r") as f:
        persona_content = f.read().strip()

    persona_block = f"{START_MARKER}\n{persona_content}\n{END_MARKER}"

    if os.path.exists(target_file):
        with open(target_file, "r") as f:
            content = f.read()

        if START_MARKER in content and END_MARKER in content:
            start_idx = content.index(START_MARKER)
            end_idx = content.index(END_MARKER) + len(END_MARKER)
            new_content = content[:start_idx] + persona_block + content[end_idx:]
        else:
            # No markers found — prepend persona block
            new_content = persona_block + "\n\n" + content
    else:
        # File doesn't exist — create it
        new_content = persona_block + "\n"

    with open(target_file, "w") as f:
        f.write(new_content)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: inject.py <persona_file> <target_file>")
        sys.exit(1)

    inject(sys.argv[1], sys.argv[2])
