"""Read BOP-Hub content off disk.

The front matter of a page *is* the record; the Markdown body below it is
curated prose that exists nowhere else. `load_documents` returns both, keyed
by the path relative to the repository root.

Everything here is root-relative rather than module-relative, so a caller can
point it at a worktree, an export staging area or a checkout other than the
one this file lives in.
"""

from __future__ import annotations

import datetime as dt
import pathlib
import re
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("pyyaml is required: pip install pyyaml")


# collection directory -> (schema file, id separator used in the filename)
COLLECTIONS = {
    "_bops": ("bop.schema.json", "-"),
    "_events": ("event.schema.json", "-"),
    "_relationships": ("relationship.schema.json", "-"),
    "_annotations": ("annotation.schema.json", "_"),
}

FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)

#: The repository root, when the caller has no opinion.
DEFAULT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent


class Report:
    """Collected problems. `where` is a path, optionally with a location."""

    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"{where}: {msg}")


def normalise_dates(obj):
    """YAML turns an unquoted 2026-11-26 into a date object; the schema wants
    a string. Normalise so curators can write dates either way."""
    if isinstance(obj, dict):
        return {k: normalise_dates(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [normalise_dates(v) for v in obj]
    if isinstance(obj, dt.datetime):
        return obj.date().isoformat()
    if isinstance(obj, dt.date):
        return obj.isoformat()
    return obj


def split_front_matter(text: str) -> tuple[str, str] | None:
    """Return (front_matter_yaml, body_markdown), or None if there is no
    front matter. The body keeps its leading newlines stripped but is
    otherwise verbatim."""
    match = FRONT_MATTER.match(text)
    if not match:
        return None
    return match.group(1), text[match.end():].lstrip("\n")


def load_vocab(root: pathlib.Path = DEFAULT_ROOT) -> dict:
    with open(root / "_data" / "vocab.yml") as fh:
        return yaml.safe_load(fh)


def load_config(root: pathlib.Path = DEFAULT_ROOT) -> dict:
    with open(root / "_config.yml") as fh:
        return yaml.safe_load(fh)


def load_documents(report: Report, root: pathlib.Path = DEFAULT_ROOT) -> tuple[dict, dict]:
    """Return ({collection_dir: {path: front_matter}}, {collection_dir: {path: body}}).

    The first element is the shape every check in `checks.py` consumes, so it
    can be built from somewhere other than the filesystem -- a database row
    set, say -- without touching the checks.
    """
    docs: dict[str, dict] = {d: {} for d in COLLECTIONS}
    bodies: dict[str, dict] = {d: {} for d in COLLECTIONS}
    for directory in COLLECTIONS:
        base = root / directory
        if not base.is_dir():
            continue
        for path in sorted(base.glob("*.md")):
            rel = path.relative_to(root)
            text = path.read_text(encoding="utf-8")
            split = split_front_matter(text)
            if split is None:
                report.error(str(rel), "no YAML front matter (file must start with ---)")
                continue
            raw, body = split
            try:
                data = yaml.safe_load(raw)
            except yaml.YAMLError as exc:
                report.error(str(rel), f"front matter is not valid YAML: {exc}")
                continue
            if not isinstance(data, dict):
                report.error(str(rel), "front matter must be a mapping")
                continue
            docs[directory][rel] = normalise_dates(data)
            bodies[directory][rel] = body
    return docs, bodies


def next_ids(docs: dict) -> dict:
    """The next free identifier per collection: highest existing + 1.

    Mirrors tools/next_id.py, which allocates the same way and leaves
    concurrent claims to collide as a git add/add conflict on the filename.
    """
    kinds = {"bop": ("_bops", "BOP", 0), "event": ("_events", "BOPE", 4),
             "relationship": ("_relationships", "BOPR", 4)}
    out = {}
    for kind, (directory, prefix, pad) in kinds.items():
        highest = 0
        for data in docs.get(directory, {}).values():
            ident = data.get("identifier")
            if isinstance(ident, str) and ident.startswith(prefix + ":"):
                tail = ident.split(":", 1)[1]
                if tail.isdigit():
                    highest = max(highest, int(tail))
        out[kind] = f"{prefix}:{highest + 1:0{pad}d}"
    return out
