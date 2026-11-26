#!/usr/bin/env python3
"""Validate BOP-Hub content: schema conformance plus referential integrity.

Run from anywhere:    python tools/validate.py [--strict]

Exits non-zero if there are errors. With --strict, warnings are errors too.

Why this exists: Jekyll will happily build a site whose cross-references are
broken. A dangling event id, an unquoted CURIE that YAML silently turned into
a mapping, or a `role:` on an event page all produce a page that renders but
says the wrong thing. This catches those before they are merged.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import pathlib
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("pyyaml is required: pip install pyyaml")

try:
    import jsonschema
except ImportError:
    sys.exit("jsonschema is required: pip install jsonschema")


ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "_data" / "schema"

# collection directory -> (schema file, id separator used in the filename)
COLLECTIONS = {
    "_bops": ("bop.schema.json", "-"),
    "_events": ("event.schema.json", "-"),
    "_relationships": ("relationship.schema.json", "-"),
    "_annotations": ("annotation.schema.json", "_"),
}

FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)


# --------------------------------------------------------------------------
# problem collection
# --------------------------------------------------------------------------
class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"{where}: {msg}")


# --------------------------------------------------------------------------
# schema preparation
# --------------------------------------------------------------------------
def load_vocab() -> dict:
    with open(ROOT / "_data" / "vocab.yml") as fh:
        return yaml.safe_load(fh)


def _validator_class():
    """Use the newest draft the installed jsonschema understands.

    Refs are inlined before validation, so no draft-specific $defs or
    resolver behaviour is relied upon.
    """
    for name in ("Draft202012Validator", "Draft201909Validator", "Draft7Validator"):
        cls = getattr(jsonschema, name, None)
        if cls is not None:
            return cls
    raise RuntimeError("no usable jsonschema validator class")


def inline_refs(node, defs, depth=0):
    """Replace {"$ref": "_defs#/$defs/x"} with the definition itself.

    Done by hand rather than with a resolver so the script behaves identically
    on jsonschema 3.x and 4.x.
    """
    if depth > 20:
        raise RuntimeError("$ref nesting too deep -- cycle in _defs.json?")
    if isinstance(node, dict):
        ref = node.get("$ref")
        if isinstance(ref, str) and ref.startswith("_defs#/$defs/"):
            key = ref.split("/")[-1]
            if key not in defs:
                raise RuntimeError(f"unknown $ref target: {ref}")
            return inline_refs(copy.deepcopy(defs[key]), defs, depth + 1)
        return {k: inline_refs(v, defs, depth + 1) for k, v in node.items()}
    if isinstance(node, list):
        return [inline_refs(v, defs, depth + 1) for v in node]
    return node


def apply_vocab(node, vocab):
    """Turn {"x-vocab": "status"} into {"enum": [...]} from vocab.yml."""
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            if k == "x-vocab":
                if v not in vocab:
                    raise RuntimeError(f"x-vocab refers to unknown list: {v}")
                out["enum"] = list(vocab[v])
            else:
                out[k] = apply_vocab(v, vocab)
        return out
    if isinstance(node, list):
        return [apply_vocab(v, vocab) for v in node]
    return node


def load_schemas(vocab) -> dict:
    with open(SCHEMA_DIR / "_defs.json") as fh:
        defs = json.load(fh)["$defs"]
    schemas = {}
    for directory, (fname, _) in COLLECTIONS.items():
        with open(SCHEMA_DIR / fname) as fh:
            schema = json.load(fh)
        schema = apply_vocab(inline_refs(schema, defs), vocab)
        schema.pop("$id", None)   # nothing resolves against it any more
        schemas[directory] = schema
    return schemas


# --------------------------------------------------------------------------
# loading content
# --------------------------------------------------------------------------
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


def load_documents(report: Report) -> dict:
    """Return {collection_dir: {path: front_matter}}."""
    docs = {d: {} for d in COLLECTIONS}
    for directory in COLLECTIONS:
        base = ROOT / directory
        if not base.is_dir():
            continue
        for path in sorted(base.glob("*.md")):
            rel = path.relative_to(ROOT)
            text = path.read_text(encoding="utf-8")
            match = FRONT_MATTER.match(text)
            if not match:
                report.error(str(rel), "no YAML front matter (file must start with ---)")
                continue
            try:
                data = yaml.safe_load(match.group(1))
            except yaml.YAMLError as exc:
                report.error(str(rel), f"front matter is not valid YAML: {exc}")
                continue
            if not isinstance(data, dict):
                report.error(str(rel), "front matter must be a mapping")
                continue
            docs[directory][rel] = normalise_dates(data)
    return docs


# --------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------
def check_schema(docs, schemas, report, validator_cls):
    for directory, entries in docs.items():
        validator = validator_cls(schemas[directory])
        for rel, data in entries.items():
            for err in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
                loc = "/".join(str(p) for p in err.path) or "(root)"
                # The single most common contributor mistake, by a mile.
                hint = ""
                if isinstance(err.instance, dict) and err.validator == "type" \
                        and err.validator_value == "string":
                    hint = ("  -> looks like an unquoted CURIE: YAML read "
                            f"{err.instance!r} as a mapping. Write it as a quoted string.")
                report.error(f"{rel} [{loc}]", err.message + hint)


def check_filenames(docs, report):
    for directory, (_, sep) in COLLECTIONS.items():
        for rel, data in docs[directory].items():
            ident = data.get("id")
            if not isinstance(ident, str):
                continue
            expected = ident.replace(":", sep)
            actual = pathlib.Path(rel).stem
            if actual != expected:
                report.error(str(rel), f"filename must match id: expected {expected}.md for id {ident!r}")


def check_duplicate_ids(docs, report):
    seen: dict[str, str] = {}
    for entries in docs.values():
        for rel, data in entries.items():
            ident = data.get("id")
            if not isinstance(ident, str):
                continue
            if ident in seen:
                report.error(str(rel), f"duplicate id {ident!r}, already used by {seen[ident]}")
            else:
                seen[ident] = str(rel)
    return seen


def check_no_role_on_events(docs, report):
    """An event is an outcome in one BOP and an intermediate key event in
    another, so a role on the event page is always wrong."""
    for rel, data in docs["_events"].items():
        if "role" in data:
            report.error(str(rel), "events must not carry `role:` -- role is per-BOP and belongs "
                                   "in that BOP's `events:` list")


def check_dates(docs, report):
    for entries in docs.values():
        for rel, data in entries.items():
            parsed = {}
            for key in ("created", "modified"):
                raw = data.get(key)
                if raw is None:
                    continue
                try:
                    parsed[key] = dt.date.fromisoformat(str(raw))
                except ValueError:
                    report.error(str(rel), f"{key} is not an ISO date (YYYY-MM-DD): {raw!r}")
            if "created" in parsed and "modified" in parsed and parsed["modified"] < parsed["created"]:
                report.error(str(rel), f"modified ({parsed['modified']}) is before created ({parsed['created']})")


def check_references_resolve(docs, report):
    events = {d["id"]: rel for rel, d in docs["_events"].items() if isinstance(d.get("id"), str)}
    kers = {d["id"]: (rel, d) for rel, d in docs["_relationships"].items() if isinstance(d.get("id"), str)}

    # relationships point at real events, and not at themselves
    for rel, data in docs["_relationships"].items():
        up, down = data.get("upstream_event"), data.get("downstream_event")
        for label, ident in (("upstream_event", up), ("downstream_event", down)):
            if isinstance(ident, str) and ident not in events:
                report.error(str(rel), f"{label} {ident} has no page in _events/")
        if up and up == down:
            report.error(str(rel), "upstream_event and downstream_event are the same event")

    for rel, data in docs["_bops"].items():
        listed = []
        for item in data.get("events") or []:
            ident = item.get("event") if isinstance(item, dict) else None
            if not isinstance(ident, str):
                continue
            listed.append(ident)
            if ident not in events:
                report.error(str(rel), f"events[] references {ident}, which has no page in _events/")
        dupes = {i for i in listed if listed.count(i) > 1}
        for ident in sorted(dupes):
            report.error(str(rel), f"event {ident} is listed more than once")

        roles = [i.get("role") for i in (data.get("events") or []) if isinstance(i, dict)]
        if roles.count("initiating") == 0:
            report.error(str(rel), "no event has role `initiating`")
        if roles.count("outcome") == 0:
            report.error(str(rel), "no event has role `outcome`")
        if roles.count("outcome") > 1:
            report.warn(str(rel), f"{roles.count('outcome')} events have role `outcome`; "
                                  "a BOP normally has one beneficial outcome")

        in_bop = set(listed)
        for item in data.get("relationships") or []:
            ident = item.get("ker") if isinstance(item, dict) else None
            if not isinstance(ident, str):
                continue
            if ident not in kers:
                report.error(str(rel), f"relationships[] references {ident}, which has no page "
                                       "in _relationships/")
                continue
            _, ker = kers[ident]
            for label in ("upstream_event", "downstream_event"):
                endpoint = ker.get(label)
                if isinstance(endpoint, str) and endpoint not in in_bop:
                    report.error(str(rel), f"{ident} has {label} {endpoint}, which is not in this "
                                           "BOP's events[] list")


def check_curies(docs, config, vocab, report):
    slots = config.get("annotation_slots") or []
    prefixes = set(vocab.get("curie_prefixes") or [])
    annotations = {d["id"]: d for d in docs["_annotations"].values() if isinstance(d.get("id"), str)}

    # annotation pages declare slots that actually exist
    for rel, data in docs["_annotations"].items():
        for slot in data.get("slot") or []:
            if slot not in slots:
                report.error(str(rel), f"slot {slot!r} is not in site.annotation_slots "
                                       f"({', '.join(slots)})")

    for directory in ("_bops", "_events", "_relationships"):
        for rel, data in docs[directory].items():
            for slot in slots:
                for curie in data.get(slot) or []:
                    if not isinstance(curie, str):
                        continue
                    prefix = curie.split(":", 1)[0]
                    if curie in annotations:
                        declared = annotations[curie].get("slot") or []
                        if slot not in declared:
                            report.warn(str(rel), f"{curie} is used in `{slot}` but its annotation "
                                                  f"page declares slot {declared}")
                    elif prefix not in prefixes:
                        report.error(str(rel), f"{curie} uses prefix {prefix!r}, which is neither in "
                                               "vocab.yml curie_prefixes nor backed by an "
                                               "_annotations page")
                    else:
                        report.warn(str(rel), f"{curie} has no page in _annotations/, so it will "
                                              "render as a dead chip")


def check_orphans(docs, report):
    used_events, used_kers = set(), set()
    for data in docs["_bops"].values():
        for item in data.get("events") or []:
            if isinstance(item, dict) and isinstance(item.get("event"), str):
                used_events.add(item["event"])
        for item in data.get("relationships") or []:
            if isinstance(item, dict) and isinstance(item.get("ker"), str):
                used_kers.add(item["ker"])

    for rel, data in docs["_events"].items():
        if isinstance(data.get("id"), str) and data["id"] not in used_events:
            report.warn(str(rel), f"{data['id']} is not used by any BOP")
    for rel, data in docs["_relationships"].items():
        if isinstance(data.get("id"), str) and data["id"] not in used_kers:
            report.warn(str(rel), f"{data['id']} is not used by any BOP")


def check_reuse_hints(docs, report):
    """Nudge towards interoperability: an event with no external anchor at all
    is either genuinely novel or a near-duplicate of something in AOP-Wiki."""
    for rel, data in docs["_events"].items():
        anchors = ("aopwiki_ke", "aopwiki_mirror_ke", "wikipathways", "external_ids", "process")
        if not any(data.get(a) for a in anchors):
            report.warn(str(rel), "no aopwiki_ke, wikipathways, external_ids or process term -- "
                                  "search AOP-Wiki before minting a new event")


def check_graph(docs, report):
    """Within a BOP, the edges must form a DAG and reach the outcome."""
    kers = {d["id"]: d for d in docs["_relationships"].values() if isinstance(d.get("id"), str)}
    for rel, data in docs["_bops"].items():
        edges = []
        for item in data.get("relationships") or []:
            ker = kers.get(item.get("ker")) if isinstance(item, dict) else None
            if ker and ker.get("upstream_event") and ker.get("downstream_event"):
                edges.append((ker["upstream_event"], ker["downstream_event"]))
        if not edges:
            continue

        adj: dict[str, list[str]] = {}
        for up, down in edges:
            adj.setdefault(up, []).append(down)

        WHITE, GREY, BLACK = 0, 1, 2
        colour: dict[str, int] = {}

        def visit(node, trail):
            colour[node] = GREY
            for nxt in adj.get(node, []):
                state = colour.get(nxt, WHITE)
                if state == GREY:
                    cycle = " -> ".join(trail + [node, nxt])
                    report.error(str(rel), f"relationship edges form a cycle: {cycle}")
                    continue
                if state == WHITE:
                    visit(nxt, trail + [node])
            colour[node] = BLACK

        for node in list(adj):
            if colour.get(node, WHITE) == WHITE:
                visit(node, [])

        connected = {n for edge in edges for n in edge}
        for item in data.get("events") or []:
            if isinstance(item, dict) and item.get("event") and item["event"] not in connected:
                report.warn(str(rel), f"{item['event']} is listed but no relationship connects it")


# --------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = parser.parse_args()

    report = Report()
    vocab = load_vocab()
    with open(ROOT / "_config.yml") as fh:
        config = yaml.safe_load(fh)
    schemas = load_schemas(vocab)
    validator_cls = _validator_class()

    docs = load_documents(report)

    check_schema(docs, schemas, report, validator_cls)
    check_filenames(docs, report)
    check_duplicate_ids(docs, report)
    check_no_role_on_events(docs, report)
    check_dates(docs, report)
    check_references_resolve(docs, report)
    check_curies(docs, config, vocab, report)
    check_orphans(docs, report)
    check_reuse_hints(docs, report)
    check_graph(docs, report)

    counts = {d.lstrip("_"): len(v) for d, v in docs.items()}
    print(f"BOP-Hub content: " + ", ".join(f"{v} {k}" for k, v in counts.items()))
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
