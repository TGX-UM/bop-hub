#!/usr/bin/env python3
"""Allocate the next free identifier in a BOP-Hub collection.

    python tools/next_id.py bop            -> BOP:2
    python tools/next_id.py event          -> BOPE:0010
    python tools/next_id.py relationship   -> BOPR:0003
    python tools/next_id.py event -n 5     -> five consecutive ids

Allocation is simply "highest existing + 1". Concurrent pull requests that
both claim the same number collide as a git add/add conflict on the filename,
which is the behaviour we want: identifiers are never silently reused.

The highest-existing scan reads the `identifier:` in each record's front
matter via tools/bophub, not the filename, so a file whose name and
identifier disagree cannot quietly shift the next allocation. The two are
required to match anyway -- tools/validate.py errors otherwise.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from bophub import load  # noqa: E402

KINDS = {
    #            directory          prefix   zero-padding
    "bop": ("_bops", "BOP", 0),
    "event": ("_events", "BOPE", 4),
    "relationship": ("_relationships", "BOPR", 4),
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("kind", choices=sorted(KINDS))
    parser.add_argument("-n", "--count", type=int, default=1, help="how many ids to allocate")
    parser.add_argument("--filename", action="store_true",
                        help="print the filename to create instead of the id")
    parser.add_argument("--root", type=pathlib.Path, default=load.DEFAULT_ROOT,
                        help="repository root to scan (default: the one this script is in)")
    args = parser.parse_args()

    if args.count < 1:
        print("--count must be at least 1", file=sys.stderr)
        return 2

    report = load.Report()
    docs, _ = load.load_documents(report, args.root.resolve())
    if report.errors:
        for line in report.errors:
            print(f"ERROR    {line}", file=sys.stderr)
        print("content does not load; fix it before allocating identifiers", file=sys.stderr)
        return 1

    directory, prefix, pad = KINDS[args.kind]
    start = int(load.next_ids(docs)[args.kind].split(":", 1)[1])

    for number in range(start, start + args.count):
        body = f"{number:0{pad}d}" if pad else str(number)
        if args.filename:
            print(f"{directory}/{prefix}-{body}.md")
        else:
            print(f"{prefix}:{body}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
