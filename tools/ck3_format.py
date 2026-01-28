#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path

INDENT = "\t"   # CK3 GUI often uses tabs; change to "    " if you want spaces.
NEWLINE = "\n"

def format_paradox(text: str) -> str:
    out: list[str] = []
    indent = 0

    in_string = False
    escape = False
    at_line_start = True

    def write(s: str) -> None:
        nonlocal at_line_start
        if s:
            out.append(s)
            at_line_start = False

    def newline() -> None:
        nonlocal at_line_start
        # trim trailing spaces/tabs before newline
        while out and out[-1] in (" ", "\t"):
            out.pop()
        out.append(NEWLINE)
        at_line_start = True

    def write_indent() -> None:
        if at_line_start:
            out.append(INDENT * max(indent, 0))

    i = 0
    n = len(text)

    while i < n:
        ch = text[i]

        # Handle string state
        if in_string:
            write(ch)
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            i += 1
            continue

        # Start of string
        if ch == '"':
            write_indent()
            write(ch)
            in_string = True
            i += 1
            continue

        # Line comments (CK3/PDX uses #)
        if ch == "#":
            write_indent()
            # copy until newline
            while i < n and text[i] != "\n":
                write(text[i])
                i += 1
            continue

        # Newlines: collapse multiple blank lines a bit (keep at most 1 blank line)
        if ch == "\n":
            newline()
            # skip additional consecutive newlines
            j = i + 1
            blank_count = 0
            while j < n and text[j] == "\n":
                blank_count += 1
                j += 1
            i += 1 + blank_count
            continue

        # Skip stray carriage returns
        if ch == "\r":
            i += 1
            continue

        # Skip leading whitespace at line start (we control indent)
        if at_line_start and ch in (" ", "\t"):
            i += 1
            continue

        if ch == "{":
            write_indent()
            write("{")
            # newline()
            indent += 1
            i += 1
            continue

        if ch == "}":
            # ensure we close on its own line
            if not at_line_start:
                newline()
            indent -= 1
            write_indent()
            write("}")
            # newline()
            i += 1
            continue

        # Default: copy character, but ensure indent at line start
        write_indent()
        write(ch)
        i += 1

    # Ensure file ends with newline
    if not out or out[-1] != NEWLINE:
        out.append(NEWLINE)

    return "".join(out)

def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: ck3_format.py <file1> [file2 ...]  (formats in-place)")
        return 2

    for p in map(Path, sys.argv[1:]):
        if not p.exists() or not p.is_file():
            print(f"Skip (not a file): {p}", file=sys.stderr)
            continue
        original = p.read_text(encoding="utf-8", errors="replace")
        formatted = format_paradox(original)
        if formatted != original:
            p.write_text(formatted, encoding="utf-8")
            print(f"Formatted: {p}")
        else:
            print(f"Unchanged: {p}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
