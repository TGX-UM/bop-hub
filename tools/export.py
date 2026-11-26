#!/usr/bin/env python3
"""Publish the repository as a read API under api/v1/.

    python tools/export.py --out _site/api/v1

The repository is the database; this is the published, machine-readable view
of it. Everything comes from tools/bophub, so the API cannot disagree with
what tools/validate.py checked -- and the export refuses to run at all if the
content has errors.

What it writes:

    index.json          counts, the commit, next free identifiers, the
                        content digest
    graph.json          every record in all four collections, including the
                        Markdown body, with each cited relationship's
                        endpoints joined in
    bops.json           one file per collection, same records
    events.json
    relationships.json
    annotations.json
    bops/BOP-1.json     one file per record
    events/...
    schema/bop.json     the normative schemas with $refs inlined and x-vocab
                        expanded to enums -- the same objects this script
                        validated against, so a browser using Ajv runs the
                        same rules rather than a second copy of them
    vocab.json          the controlled vocabularies
    manifest.json       sha256 per file, plus a digest over all of them

NOTE on ordering: Jekyll deletes anything in the destination that it did not
generate, so this must run AFTER `jekyll build`, not before. Writing into
_site first and building second silently throws the API away.

NOTE on the digest: `generated` appears in index.json and nowhere else, so
manifest.json's content_digest is a fingerprint of the content itself and is
identical across two builds of the same commit. manifest.json excludes itself
and index.json for the same reason.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from bophub import checks, load, schema as schema_mod  # noqa: E402

#: collection directory -> (key in the dump, url segment)
PUBLISHED = {
    "_bops": ("bops", "bops"),
    "_events": ("events", "events"),
    "_relationships": ("relationships", "relationships"),
    "_annotations": ("annotations", "annotations"),
}


def commit_sha(root: pathlib.Path) -> str | None:
    """The commit being published. Falls back to the CI-provided sha when the
    checkout is not a git tree (an export from a staging directory)."""
    try:
        out = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"],
                             capture_output=True, text=True, timeout=10)
        if out.returncode == 0:
            return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return os.environ.get("GITHUB_SHA")


def slug(rel: pathlib.Path) -> str:
    return pathlib.Path(rel).stem


def record(rel, data, body, segment, canonical_base, site_base):
    """One published record: its front matter, its body, and where it lives.

    `page_iri` is always this record's canonical BOP-Hub IRI, computed from
    the permalink against canonical_base and never stored in a page. `iri` is
    left to the front matter where it has one -- on an annotation that is the
    ontology term's own PURL, which is the right @id for a page *about* that
    term, and it must not be clobbered by the page's address.
    """
    name = slug(rel)
    path = f"/{segment}/{name}/"
    out = {
        "identifier": data.get("identifier"),
        "page_iri": f"{canonical_base}{path}",
        "url": f"{site_base}{path}",
        "source_path": str(rel),
    }
    if "iri" not in data:
        out["iri"] = out["page_iri"]
    for key, value in data.items():
        if key == "layout":         # Jekyll plumbing, not content
            continue
        out[key] = value
    out["body_markdown"] = body
    return out


def join_bop_edges(bop, relationships_by_id):
    """Give a BOP's events and cited relationships an explicit position, and
    join each cited relationship's endpoints in.

    Position matters: list order is the pathway spine, it is rendered on every
    BOP page, and it is not recoverable afterwards. The graph branches, so a
    topological sort is not unique, and ordering by identifier only works
    while BOP:1 is the only pathway.
    """
    events = []
    for i, item in enumerate(bop.get("events") or []):
        if not isinstance(item, dict):
            continue
        events.append({"position": i, "event": item.get("event"), "role": item.get("role")})

    edges = []
    for i, item in enumerate(bop.get("relationships") or []):
        if not isinstance(item, dict):
            continue
        ker = relationships_by_id.get(item.get("ker")) or {}
        entry = {
            "position": i,
            "relationship": item.get("ker"),
            "upstream_event": ker.get("upstream_event"),
            "downstream_event": ker.get("downstream_event"),
            "adjacency": ker.get("adjacency"),
            "essentiality": item.get("essentiality"),
            "confidence": item.get("confidence"),
        }
        if item.get("comment") is not None:
            entry["comment"] = item["comment"]
        edges.append(entry)

    bop["events"] = events
    bop["relationships"] = edges
    return bop


#: Fields the Liquid-rendered /api/bops.json and /api/events.json share with
#: api/v1. Those two endpoints are a published contract -- the footer and
#: about.md link them -- so they stay, rendered by Jekyll as before. This is
#: the guard that stops the two code paths drifting apart unnoticed.
LEGACY_SHARED = {
    "bops": ("iri", "url", "title", "status", "overall_confidence", "modified",
             "interventions", "taxa", "sex", "life_stage", "diseases", "phenotypes"),
    "events": ("iri", "url", "title", "biological_level", "process", "object", "action",
               "aopwiki_ke", "aopwiki_mirror_ke", "status", "modified", "taxa"),
    "relationships": ("iri", "url", "title", "upstream_event", "downstream_event",
                      "adjacency", "evidence", "status", "modified"),
}


def check_legacy(api_dir: pathlib.Path, collections: dict) -> list[str]:
    """Compare the Jekyll-rendered legacy dumps against this export.

    Returns a list of disagreements; an empty list means the two agree on
    every field they share. Silently returns nothing if the legacy files are
    absent, so the exporter still works outside a built site.
    """
    legacy_files = {"bops": api_dir / "bops.json", "events": api_dir / "events.json"}
    if not all(p.is_file() for p in legacy_files.values()):
        return []

    by_id = {key: {r["identifier"]: r for r in rows} for key, rows in collections.items()}
    diffs: list[str] = []

    def compare(kind, rows):
        for row in rows:
            ident = row.get("identifier")
            mine = by_id.get(kind, {}).get(ident)
            if mine is None:
                diffs.append(f"{kind} {ident} is in the legacy dump but not in api/v1")
                continue
            for field in LEGACY_SHARED[kind]:
                if field in row and row[field] != mine.get(field):
                    diffs.append(f"{kind} {ident}.{field}: legacy={row[field]!r} "
                                 f"v1={mine.get(field)!r}")

    bops = json.loads(legacy_files["bops"].read_text())
    compare("bops", bops.get("bops") or [])
    for row in bops.get("bops") or []:
        mine = by_id.get("bops", {}).get(row.get("identifier")) or {}
        for i, (legacy, new) in enumerate(zip(row.get("events") or [],
                                              mine.get("events") or [])):
            if (legacy.get("event"), legacy.get("role")) != (new.get("event"), new.get("role")):
                diffs.append(f"bop {row.get('identifier')} events[{i}]: "
                             f"legacy={legacy} v1={new}")
        for i, (legacy, new) in enumerate(zip(row.get("relationships") or [],
                                              mine.get("relationships") or [])):
            for field in ("relationship", "upstream_event", "downstream_event",
                          "adjacency", "essentiality", "confidence"):
                if legacy.get(field) != new.get(field):
                    diffs.append(f"bop {row.get('identifier')} relationships[{i}].{field}: "
                                 f"legacy={legacy.get(field)!r} v1={new.get(field)!r}")

    events = json.loads(legacy_files["events"].read_text())
    compare("events", events.get("events") or [])
    compare("relationships", events.get("relationships") or [])
    return diffs


def write_json(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False,
                               sort_keys=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=pathlib.Path, required=True,
                        help="directory to write api/v1 into")
    parser.add_argument("--root", type=pathlib.Path, default=load.DEFAULT_ROOT,
                        help="repository root to export (default: the one this script is in)")
    parser.add_argument("--site-url", default=None,
                        help="the site's base URL, overriding url+baseurl from _config.yml. "
                             "In CI pass ${{ steps.pages.outputs.base_url }} so the `url` "
                             "fields match the baseurl Jekyll actually built with.")
    args = parser.parse_args()

    root = args.root.resolve()
    out = args.out.resolve()

    report = load.Report()
    vocab = load.load_vocab(root)
    config = load.load_config(root)
    schemas = schema_mod.load_schemas(vocab, root)
    docs, bodies = load.load_documents(report, root)
    checks.run_all(docs, schemas, config, vocab, report,
                   schema_mod.validator_class(), schema_mod.format_checker())

    if report.errors:
        for line in report.errors:
            print(f"ERROR    {line}", file=sys.stderr)
        print(f"\nrefusing to export {len(report.errors)} error(s)", file=sys.stderr)
        return 1
    for line in report.warnings:
        print(f"WARNING  {line}", file=sys.stderr)

    canonical_base = (config.get("canonical_base") or "").rstrip("/")
    if args.site_url:
        site_base = args.site_url.rstrip("/")
    else:
        site_base = ((config.get("url") or "").rstrip("/")
                     + (config.get("baseurl") or "").rstrip("/"))

    relationships_by_id = {
        d["identifier"]: d for d in docs["_relationships"].values()
        if isinstance(d.get("identifier"), str)
    }

    collections = {}
    for directory, (key, segment) in PUBLISHED.items():
        rows = []
        for rel, data in docs[directory].items():
            row = record(rel, data, bodies[directory].get(rel, ""),
                         segment, canonical_base, site_base)
            if directory == "_bops":
                row = join_bop_edges(row, relationships_by_id)
            rows.append(row)
        rows.sort(key=lambda r: str(r.get("identifier") or ""))
        collections[key] = rows

    counts = {k: len(v) for k, v in collections.items()}
    generated = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    sha = commit_sha(root)

    envelope = {
        "@context": f"{site_base}/assets/context.jsonld",
        "canonical_base": canonical_base,
        "license": {"content": "CC0-1.0", "code": "MIT"},
        "commit": sha,
        "counts": counts,
    }

    # graph.json -- the whole thing, which is what most consumers want: the
    # full dump is small enough to download and query in memory.
    write_json(out / "graph.json", {**envelope, **collections})

    # per collection, and per record
    for key, rows in collections.items():
        write_json(out / f"{key}.json", {**envelope, key: rows})
        for row in rows:
            name = pathlib.Path(row["source_path"]).stem
            write_json(out / key / f"{name}.json", {**envelope, "record": row})

    # the rules, as actually enforced
    for directory, (key, _) in PUBLISHED.items():
        write_json(out / "schema" / f"{key[:-1] if key.endswith('s') else key}.json",
                   schemas[directory])
    write_json(out / "vocab.json", vocab)

    # fixity over everything but index.json and manifest.json
    files = {}
    for path in sorted(out.rglob("*.json")):
        name = str(path.relative_to(out))
        if name in ("index.json", "manifest.json"):
            continue
        files[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    tree = hashlib.sha256(
        "".join(f"{n}\0{h}\n" for n, h in sorted(files.items())).encode()
    ).hexdigest()
    write_json(out / "manifest.json", {
        "algorithm": "sha256",
        "excludes": ["index.json", "manifest.json"],
        "content_digest": tree,
        "files": files,
    })

    write_json(out / "index.json", {
        **envelope,
        "generated": generated,
        "content_digest": tree,
        "next_ids": load.next_ids(docs),
        "endpoints": sorted(
            str(p.relative_to(out)) for p in out.rglob("*.json") if p.parent == out
        ),
    })

    drift = check_legacy(out.parent, collections)
    if drift:
        for line in drift:
            print(f"DRIFT    {line}", file=sys.stderr)
        print(f"\n{len(drift)} disagreement(s) between the legacy /api dumps and api/v1",
              file=sys.stderr)
        return 1

    print(f"exported {sum(counts.values())} records to {out}")
    print("counts: " + ", ".join(f"{v} {k}" for k, v in counts.items()))
    print(f"content digest: {tree[:16]}…")
    return 0


if __name__ == "__main__":
    sys.exit(main())
