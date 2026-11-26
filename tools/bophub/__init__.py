"""BOP-Hub content model: load it, resolve its schemas, check it.

The repository is the database. This package is the single reader of it, so
that the validator, the API exporter and anything built later all see the
same records and run the same rules.

    from bophub import load, schema, checks

    report = load.Report()
    docs, bodies = load.load_documents(report, root)
    vocab = load.load_vocab(root)
    checks.run_all(docs, schema.load_schemas(vocab, root), load.load_config(root),
                   vocab, report, schema.validator_class(), schema.format_checker())
"""

from . import checks, load, schema  # noqa: F401

__all__ = ["checks", "load", "schema"]
