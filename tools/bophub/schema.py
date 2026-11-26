"""Turn the normative JSON Schemas into something a validator can run.

Two transforms, in this order:

  inline_refs   {"$ref": "_defs#/$defs/x"} -> the definition itself
  apply_vocab   {"x-vocab": "status"}      -> {"enum": [...]} from vocab.yml

Both are applied before validation here and before the schemas are published
to `api/v1/schema/`, so a browser validating with Ajv is running exactly the
rules this package runs -- there is no second copy of them anywhere.
"""

from __future__ import annotations

import copy
import json
import pathlib
import sys

from .load import COLLECTIONS, DEFAULT_ROOT

try:
    import jsonschema
except ImportError:  # pragma: no cover
    sys.exit("jsonschema is required: pip install jsonschema")


def validator_class():
    """Use the newest draft the installed jsonschema understands.

    Refs are inlined before validation, so no draft-specific $defs or
    resolver behaviour is relied upon.
    """
    for name in ("Draft202012Validator", "Draft201909Validator", "Draft7Validator"):
        cls = getattr(jsonschema, name, None)
        if cls is not None:
            return cls
    raise RuntimeError("no usable jsonschema validator class")


def format_checker():
    """A FormatChecker so `"format": "date"` is actually enforced.

    Without it jsonschema ignores `format` entirely. The browser side needs
    ajv-formats for the same reason; see api.md.
    """
    return jsonschema.FormatChecker()


def inline_refs(node, defs, depth=0):
    """Replace {"$ref": "_defs#/$defs/x"} with the definition itself.

    Done by hand rather than with a resolver so behaviour is identical on
    jsonschema 3.x and 4.x.
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


def load_schemas(vocab: dict, root: pathlib.Path = DEFAULT_ROOT) -> dict:
    """{collection_dir: resolved schema}, refs inlined and vocab expanded."""
    schema_dir = root / "_data" / "schema"
    with open(schema_dir / "_defs.json") as fh:
        defs = json.load(fh)["$defs"]
    schemas = {}
    for directory, (fname, _) in COLLECTIONS.items():
        with open(schema_dir / fname) as fh:
            schema = json.load(fh)
        schema = apply_vocab(inline_refs(schema, defs), vocab)
        schema.pop("$id", None)   # nothing resolves against it any more
        schemas[directory] = schema
    return schemas
