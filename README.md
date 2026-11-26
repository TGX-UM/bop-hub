# BOP-Hub

**A community-curated knowledge base of Beneficial Outcome Pathways: causal chains
linking a beneficial exposure or intervention, through measurable key events, to a
benefit to health.** It is the beneficial counterpart to
[AOP-Wiki](https://aopwiki.org/), and it uses the same event-and-relationship grammar
so that beneficial and adverse pathways can be read together.

**→ [tgx-um.github.io/bop-hub](https://tgx-um.github.io/bop-hub/)**

The one pathway curated so far: [**BOP:1** — energy deficit from fasting leading to
resolution of metabolic dysfunction-associated steatotic liver
disease](https://tgx-um.github.io/bop-hub/bops/BOP-1/).

## Status: v0

One pathway, 13 events, 19 relationships. **The schema is not yet stable** and breaking
changes to the content model should be expected before 1.0. Identifiers are the
exception: once issued, they are never reused or renumbered. The schema will be frozen
when a second independently curated pathway has gone in without needing a change to it.

## What it is for, and what it is not

For: structuring a mechanistic hypothesis so its parts can be tested separately;
mapping where the evidence for an intervention is strong and where it is thin; anchoring
omics and other new-approach-methodology data to specific events; and reading beneficial
pathways against the adverse ones they meet.

Not for, and this matters more here than it would for a resource about harm:

- **Not medical advice.** No page is a recommendation to undertake any intervention.
- **Not health-claim authorisation.** A pathway here carries no regulatory status.
- **Not a substitute for regulatory assessment** by EFSA or any other authority.
- **Not a clinical guideline, and not evidence of safety.** Some pathways describe
  interventions that harm some people; where known, the page says so.

A pathway asserts that an intervention *can plausibly* lead to an outcome in at least
some people, with the strength of evidence stated. Not that it will, or that it is advisable.

## The content model

Four kinds of page, and one rule that makes separating them worthwhile.

| | Lives in | Holds |
|---|---|---|
| **Pathway** | `_bops/BOP-1.md` | An assembly of events into a chain, plus how essential each link is *to this chain* |
| **Event** | `_events/BOPE-0001.md` | A measurable biological change. Reusable across pathways |
| **Relationship** | `_relationships/BOPR-0001.md` | A causal link between two events, with the evidence for the link itself |
| **Term** | `_annotations/MONDO_0013209.md` | An ontology concept used to say where a pathway applies |

**The rule: the part an event plays belongs to the pathway, not to the event.** Improved
insulin sensitivity is the endpoint of one pathway and a step along the way in another.
Recording the role on the event page would make that impossible, and it is the whole
reason events can be shared. The validator rejects a `role:` on an event page.

Evidence is graded in two layers, following AOP practice. A relationship page carries the
*intrinsic* evidence for the causal link — biological plausibility, empirical support,
quantitative understanding. A pathway that uses the link adds its own *essentiality* and
*confidence*, because the same step can be load-bearing in one pathway and incidental in
another.

The normative definition is `_data/schema/*.json`; `_data/vocab.yml` holds the controlled
vocabularies. [`_bops/BOP-1.md`](_bops/BOP-1.md) is the readable one.

## Contributing

**You do not need to know Jekyll, or write any YAML.**
[Open an issue describing the pathway and its evidence](https://github.com/TGX-UM/bop-hub/issues/new/choose)
and a maintainer will write it up with you. That is the expected route for domain
experts, not a fallback. If you would rather do it yourself,
[CONTRIBUTING.md](CONTRIBUTING.md) walks through adding a pathway from start to finish.

Pull requests are reviewed by a maintainer and checked automatically against the content
schema. Everything starts at `status: draft`; promotion beyond draft needs review by a
curator other than the author.

## Machine-readable access

- [`/api/bops.json`](https://tgx-um.github.io/bop-hub/api/bops.json) — pathways with their events, edges and applicability
- [`/api/events.json`](https://tgx-um.github.io/bop-hub/api/events.json) — events and relationships
- [`/assets/context.jsonld`](https://tgx-um.github.io/bop-hub/assets/context.jsonld) — JSON-LD context mapping the front matter onto the AOP ontology, Dublin Core and SKOS

Content IRIs are computed against `https://w3id.org/bop-hub` rather than the hosting URL,
so moving to a custom domain will not invalidate one. Registering that namespace is a
pending task; until then the IRIs are stable but not yet resolvable.

## Licensing

Curated content is **CC0 1.0** ([LICENSE-CONTENT](LICENSE-CONTENT)) — reuse it freely,
no attribution required, though citing us helps ([CITATION.cff](CITATION.cff)). The site
code is **MIT** ([LICENSE](LICENSE)). The scaffolding derives from
[wikipathways/Jiffy](https://github.com/wikipathways/Jiffy); see [NOTICE](NOTICE).

Note that AOP-Wiki content is CC BY-SA 4.0. Cross-referencing its identifiers is fine;
copying its descriptive prose into this repository is not. Write your own.

## Local development

No Ruby on your machine required:

```bash
docker run --rm -u "$(id -u):$(id -g)" -v "$PWD":/app -w /app -p 4000:4000 \
  -e BUNDLE_PATH=/app/vendor/bundle -e HOME=/tmp ruby:3.3 \
  bash -lc "bundle install && bundle exec jekyll serve --host 0.0.0.0"
```

Then open <http://127.0.0.1:4000/bop-hub/>. Note that `_config.yml` is *not* reloaded
while the server runs — restart it after changing that file.

Validate content and allocate identifiers:

```bash
pip install -r tools/requirements.txt
python tools/validate.py            # --strict to fail on warnings too
python tools/next_id.py event -n 3  # next free event identifiers
```

The site builds with Jekyll 4 directly, **not** the `github-pages` gem: those pins exist
to mirror GitHub's legacy branch-based builder, and this site builds in its own Actions
workflow. The gem would also pin `liquid` 4.0.3, which calls `Object#tainted?`, removed
in Ruby 3.2.

## Maintainers

Department of Translational Genomics, Maastricht University.
Marvin Martens ([@marvinm2](https://github.com/marvinm2),
[ORCID 0000-0003-2230-0840](https://orcid.org/0000-0003-2230-0840)).
