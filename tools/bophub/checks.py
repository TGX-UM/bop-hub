"""Content checks beyond schema conformance.

Every function here takes the `docs` mapping that `load.load_documents`
returns -- {collection_dir: {path: front_matter}} -- and a `Report`. None of
them touch the filesystem, so the same checks run over a database row set,
a staged export or a worktree without modification.

What is NOT expressible as a schema or a foreign key, and so genuinely needs
this module: the per-BOP DAG cycle walk, the at-least-one-outcome rule, and
the advisory warnings (orphans, reuse hints, CURIE backing).
"""

from __future__ import annotations

import datetime as dt
import pathlib

from .load import COLLECTIONS


def check_schema(docs, schemas, report, validator_cls, format_checker=None):
    for directory, entries in docs.items():
        validator = validator_cls(schemas[directory], format_checker=format_checker)
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
            ident = data.get("identifier")
            if not isinstance(ident, str):
                continue
            expected = ident.replace(":", sep)
            actual = pathlib.Path(rel).stem
            if actual != expected:
                report.error(str(rel), f"filename must match identifier: expected {expected}.md for {ident!r}")


def check_duplicate_ids(docs, report):
    seen: dict[str, str] = {}
    for entries in docs.values():
        for rel, data in entries.items():
            ident = data.get("identifier")
            if not isinstance(ident, str):
                continue
            if ident in seen:
                report.error(str(rel), f"duplicate identifier {ident!r}, already used by {seen[ident]}")
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
    """Only the ordering rule. Whether a date parses at all is `format: date`
    in the schema, enforced by the FormatChecker, so it is not repeated here."""
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
                    continue   # the schema reports this
            if "created" in parsed and "modified" in parsed and parsed["modified"] < parsed["created"]:
                report.error(str(rel), f"modified ({parsed['modified']}) is before created ({parsed['created']})")


def check_references_resolve(docs, report):
    events = {d["identifier"]: rel for rel, d in docs["_events"].items() if isinstance(d.get("identifier"), str)}
    kers = {d["identifier"]: (rel, d) for rel, d in docs["_relationships"].items() if isinstance(d.get("identifier"), str)}

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
        cited = []
        for item in data.get("relationships") or []:
            ident = item.get("ker") if isinstance(item, dict) else None
            if not isinstance(ident, str):
                continue
            cited.append(ident)
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
        # Mirrors the duplicate-event rule. Without it a (bop, ker) primary key
        # in any downstream store would reject input this validator accepted.
        ker_dupes = {i for i in cited if cited.count(i) > 1}
        for ident in sorted(ker_dupes):
            report.error(str(rel), f"relationship {ident} is listed more than once")


def check_curies(docs, config, vocab, report):
    slots = config.get("annotation_slots") or []
    prefixes = set(vocab.get("curie_prefixes") or [])
    annotations = {d["identifier"]: d for d in docs["_annotations"].values() if isinstance(d.get("identifier"), str)}

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
        if isinstance(data.get("identifier"), str) and data["identifier"] not in used_events:
            report.warn(str(rel), f"{data['identifier']} is not used by any BOP")
    for rel, data in docs["_relationships"].items():
        if isinstance(data.get("identifier"), str) and data["identifier"] not in used_kers:
            report.warn(str(rel), f"{data['identifier']} is not used by any BOP")


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
    kers = {d["identifier"]: d for d in docs["_relationships"].values() if isinstance(d.get("identifier"), str)}
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


#: Every check, in the order they are run. Keeping the order here rather than
#: in a CLI means the portal and CI cannot drift apart on it.
def run_all(docs, schemas, config, vocab, report, validator_cls, format_checker=None):
    check_schema(docs, schemas, report, validator_cls, format_checker)
    check_filenames(docs, report)
    check_duplicate_ids(docs, report)
    check_no_role_on_events(docs, report)
    check_dates(docs, report)
    check_references_resolve(docs, report)
    check_curies(docs, config, vocab, report)
    check_orphans(docs, report)
    check_reuse_hints(docs, report)
    check_graph(docs, report)
    return report
