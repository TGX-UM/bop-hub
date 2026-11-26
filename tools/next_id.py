#!/usr/bin/env python3
"""Allocate the next free identifier in a BOP-Hub collection.

    python tools/next_id.py bop            -> BOP:2
    python tools/next_id.py event          -> BOPE:0010
    python tools/next_id.py relationship   -> BOPR:0003
    python tools/next_id.py event -n 5     -> five consecutive ids

Allocation is simply "highest existing + 1". Concurrent pull requests that
both claim the same number collide as a git add/add conflict on the filename,
which is the behaviour we want: identifiers are never silently reused.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

KINDS = {
    #            directory          prefix   zero-padding
    "bop": ("_bops", "BOP", 0),
    "event": ("_events", "BOPE", 4),
    "relationship": ("_relationships", "BOPR", 4),
}


def highest(directory: str, prefix: str) -> int:
    base = ROOT / directory
    if not base.is_dir():
        return 0
    pattern = re.compile(rf"^{re.escape(prefix)}-(\d+)$")
    numbers = [
        int(m.group(1))
        for path in base.glob("*.md")
        if (m := pattern.match(path.stem))
    ]
    return max(numbers, default=0)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("kind", choices=sorted(KINDS))
    parser.add_argument("-n", "--count", type=int, default=1, help="how many ids to allocate")
    parser.add_argument("--filename", action="store_true",
                        help="print the filename to create instead of the id")
    args = parser.parse_args()

    if args.count < 1:
        print("--count must be at least 1", file=sys.stderr)
        return 2

    directory, prefix, pad = KINDS[args.kind]
    start = highest(directory, prefix) + 1

    for number in range(start, start + args.count):
        body = f"{number:0{pad}d}" if pad else str(number)
        if args.filename:
            print(f"{directory}/{prefix}-{body}.md")
        else:
            print(f"{prefix}:{body}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
