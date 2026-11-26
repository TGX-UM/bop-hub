#!/usr/bin/env python3
"""Publish BOP-Hub as RDF, from the JSON the API already serves.

    python tools/export_rdf.py --graph _site/api/v1/graph.json --out _site/rdf

Shape comes from tools/export.py and meaning from assets/context.jsonld, so
there is one shaper and one mapping, not a third expression of the model.

It also writes the controlled vocabularies as SKOS. `essentiality: strong`
expands to bopv:strong via the context's @vocab, and without a concept scheme
that IRI would resolve to nothing.

The guard that matters: every key in the data must be either explicitly
defined in the context or on the bookkeeping list below. The context sets
@vocab, so an unmapped key would otherwise expand to bopv:<key> and look
mapped -- which is how `status`, `role`, `essentiality`, `evidence` and
twenty-nine others came to be absent from the context while the RDF looked
fine. A new schema field now fails this script until it is given a meaning.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from bophub import load  # noqa: E402

try:
    import rdflib
except ImportError:  # pragma: no cover
    sys.exit("rdflib is required: pip install rdflib")

BOPV = "https://w3id.org/bop-hub/vocab#"

#: Export bookkeeping, deliberately not published as RDF. ENVELOPE keys carry
#: bookkeeping all the way down, so the key scan does not descend into them;
#: the others are single keys whose values are still content (the four
#: collection keys hold the records themselves).
ENVELOPE = {"@context", "license", "counts", "next_ids", "endpoints"}
EXCLUDED = ENVELOPE | {
    "source_path", "commit", "generated", "canonical_base", "content_digest",
    "bops", "events", "relationships", "annotations",
}

#: vocab.yml list -> (skos:ConceptScheme slug, human label). curie_prefixes is
#: not a value vocabulary, so it gets no scheme.
SCHEMES = {
    "status": "Curation status",
    "role": "Role of an event within a BOP",
    "biological_level": "Level of biological organisation",
    "adjacency": "Adjacency of a relationship",
    "evidence_level": "Weight-of-evidence grade",
    "essentiality": "Essentiality of a relationship within a BOP",
    "confidence": "Confidence in a relationship within a BOP",
    "aop_relation": "How a BOP relates to an AOP",
    "modulation_direction": "Direction in which a modulating factor acts",
}


def collect_keys(node, found: set) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            found.add(key)
            if key not in ENVELOPE:
                collect_keys(value, found)
    elif isinstance(node, list):
        for value in node:
            collect_keys(value, found)


def strip(node):
    """Drop bookkeeping keys, and empty bodies: an annotation page is pure
    front matter, and `bopv:body ""` asserts nothing."""
    if isinstance(node, dict):
        return {k: strip(v) for k, v in node.items()
                if k != "source_path" and not (k == "body_markdown" and v == "")}
    if isinstance(node, list):
        return [strip(v) for v in node]
    return node


def vocab_graph(vocab: dict) -> rdflib.Graph:
    g = rdflib.Graph()
    SKOS = rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")
    g.bind("skos", SKOS)
    g.bind("bopv", rdflib.Namespace(BOPV))
    for name, label in SCHEMES.items():
        values = vocab.get(name) or []
        scheme = rdflib.URIRef(f"{BOPV}{name}")
        g.add((scheme, rdflib.RDF.type, SKOS.ConceptScheme))
        g.add((scheme, SKOS.prefLabel, rdflib.Literal(label, lang="en")))
        for value in values:
            concept = rdflib.URIRef(f"{BOPV}{value}")
            g.add((concept, rdflib.RDF.type, SKOS.Concept))
            g.add((concept, SKOS.prefLabel, rdflib.Literal(value, lang="en")))
            g.add((concept, SKOS.inScheme, scheme))
            g.add((scheme, SKOS.hasTopConcept, concept))
    return g


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--graph", type=pathlib.Path, required=True,
                        help="the api/v1/graph.json written by tools/export.py")
    parser.add_argument("--out", type=pathlib.Path, required=True,
                        help="directory to write the RDF into")
    parser.add_argument("--root", type=pathlib.Path, default=load.DEFAULT_ROOT)
    args = parser.parse_args()

    root = args.root.resolve()
    dump = json.loads(args.graph.read_text())
    context = json.loads((root / "assets" / "context.jsonld").read_text())["@context"]

    # --- the guard --------------------------------------------------------
    keys: set[str] = set()
    collect_keys(dump, keys)
    defined = {k for k in context if not k.startswith(("@", "_comment"))}
    unmapped = sorted(k for k in keys if k not in defined and k not in EXCLUDED)
    if unmapped:
        print("These keys appear in the data but have no meaning in "
              "assets/context.jsonld:", file=sys.stderr)
        for key in unmapped:
            print(f"  {key}", file=sys.stderr)
        print("\nGive each one a predicate, or add it to EXCLUDED in this script if it "
              "is bookkeeping. @vocab would otherwise expand it to bopv:<key>, which "
              "looks mapped and means nothing.", file=sys.stderr)
        return 1

    # --- the content ------------------------------------------------------
    doc = {"@context": context, "@graph": []}
    for key in ("bops", "events", "relationships", "annotations"):
        doc["@graph"].extend(strip(dump.get(key) or []))

    graph = rdflib.Graph()
    graph.parse(data=json.dumps(doc), format="json-ld")
    graph += vocab_graph(load.load_vocab(root))

    for prefix, ns in (("bop", "https://w3id.org/bop-hub/"), ("bopv", BOPV),
                       ("aopo", "http://aopkb.org/aop_ontology#"),
                       ("dcterms", "http://purl.org/dc/terms/"),
                       ("skos", "http://www.w3.org/2004/02/skos/core#"),
                       ("obo", "http://purl.obolibrary.org/obo/"),
                       ("ncit", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#"),
                       ("edam", "http://edamontology.org/"),
                       ("ncbitaxon", "http://purl.bioontology.org/ontology/NCBITAXON/"),
                       ("pav", "http://purl.org/pav/"), ("foaf", "http://xmlns.com/foaf/0.1/")):
        graph.bind(prefix, rdflib.Namespace(ns))

    args.out.mkdir(parents=True, exist_ok=True)
    for fmt, suffix in (("turtle", "ttl"), ("nt", "nt"), ("json-ld", "jsonld")):
        graph.serialize(destination=str(args.out / f"bop-hub.{suffix}"), format=fmt)

    print(f"{len(graph)} triples -> {args.out}/bop-hub.{{ttl,nt,jsonld}}")
    print(f"{len(set(graph.predicates()))} distinct predicates, "
          f"{len(set(graph.subjects()))} subjects")
    return 0


if __name__ == "__main__":
    sys.exit(main())
