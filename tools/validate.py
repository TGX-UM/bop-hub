#!/usr/bin/env python3
"""Validate BOP-Hub content: schema conformance plus referential integrity.

Run from anywhere:    python tools/validate.py [--strict] [--root PATH]

Exits non-zero if there are errors. With --strict, warnings are errors too.

Why this exists: Jekyll will happily build a site whose cross-references are
broken. A dangling event id, an unquoted CURIE that YAML silently turned into
a mapping, or a `role:` on an event page all produce a page that renders but
says the wrong thing. This catches those before they are merged.

The model and the rules live in tools/bophub/; this file is only a CLI over
them, so the same checks can run against a worktree or a database projection.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import jsonschema  # noqa: E402

from bophub import checks, load, schema as schema_mod  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    parser.add_argument("--root", type=pathlib.Path, default=load.DEFAULT_ROOT,
                        help="repository root to validate (default: the one this script is in)")
    args = parser.parse_args()

    root = args.root.resolve()
    report = load.Report()
    vocab = load.load_vocab(root)
    config = load.load_config(root)
    schemas = schema_mod.load_schemas(vocab, root)
    validator_cls = schema_mod.validator_class()

    docs, _bodies = load.load_documents(report, root)
    checks.run_all(docs, schemas, config, vocab, report,
                   validator_cls, schema_mod.format_checker())

    counts = {d.lstrip("_"): len(v) for d, v in docs.items()}
    print("BOP-Hub content: " + ", ".join(f"{v} {k}" for k, v in counts.items()))
    print(f"validator: {validator_cls.__name__} (jsonschema {jsonschema.__version__})\n")

    for line in report.warnings:
        print(f"WARNING  {line}")
    for line in report.errors:
        print(f"ERROR    {line}")

    if report.errors:
        print(f"\n{len(report.errors)} error(s), {len(report.warnings)} warning(s)")
        return 1
    if report.warnings and args.strict:
        print(f"\n0 errors, {len(report.warnings)} warning(s) -- failing because --strict")
        return 1
    print(f"\nOK: 0 errors, {len(report.warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
