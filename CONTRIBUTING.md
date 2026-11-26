# Contributing to BOP-Hub

## Three ways in, easiest first

**1. Describe the pathway and let a maintainer write it up.** This is the expected route
for domain experts, not a fallback.
[Open a "Propose a pathway" issue](https://github.com/TGX-UM/bop-hub/issues/new/choose):
tell us the intervention, the chain of events, the outcome, and the papers behind each
step. A maintainer turns that into the files and puts your name on it as curator. You
never touch YAML.

**2. Fix a page in the browser.** Every page has an "Edit this page on GitHub" link at
the bottom. Use it for a typo, a clarification, or an added reference. GitHub handles the
fork and pull request for you.

**3. Fork and curate.** Full control. The walkthrough below.

However you contribute, your git identity — the name and email on your commits — becomes
a permanent part of the public history. If you would rather not have a personal email in
there, set a different one on this repository before committing.

## Adding a pathway, start to finish

### Allocate identifiers

```bash
python tools/next_id.py bop               # BOP:2
python tools/next_id.py event -n 4        # BOPE:0014 … BOPE:0017
python tools/next_id.py relationship -n 3 # BOPR:0020 …
```

Allocation is "highest existing plus one". If two pull requests claim the same number,
git reports an add/add conflict on the filename, which is what we want: identifiers are
never silently reused. Once issued, an identifier is never reused or renumbered — a
retired page gets `status: deprecated` plus `replaced_by:`.

**The filename is the identifier.** `BOP:2` lives in `_bops/BOP-2.md`; `BOPE:0014` in
`_events/BOPE-0014.md`; `MONDO:0013209` in `_annotations/MONDO_0013209.md` — with an
underscore, because a colon in a filename breaks checkouts on Windows.

### Reuse before you mint

**Before creating an event, look for it in `_events/` and then in
[AOP-Wiki](https://aopwiki.org/events).** This is the rule that decides whether BOP-Hub
becomes interoperable or an island, so it gets its own heading.

- The event already exists in AOP-Wiki, same direction and level → create the page and
  set `aopwiki_ke: "aop.events:1312"`. You are reusing it, not re-minting it.
- AOP-Wiki has the *opposite* direction — same object, opposite action → that is **not**
  the same event. Set `aopwiki_mirror_ke:` instead. This is what makes a pathway readable
  against the adverse pathways it counteracts, and conflating the two destroys exactly
  that.
- Genuinely new → fine, but say in the page body what you searched.

The validator warns when an event has no `aopwiki_ke`, `aopwiki_mirror_ke`,
`wikipathways`, `external_ids` or `process` term. A warning, not an error: some events
really are novel. Do not silence it by inventing a match.

### Grade the evidence

Every relationship is graded on three dimensions, adapted from the modified Bradford-Hill
considerations in the
[AOP Developers' Handbook](https://aopwiki.org/handbooks/5). Use these definitions so
that grades mean the same thing across pages.

| | high | moderate | low |
|---|---|---|---|
| **Biological plausibility** | The link follows from well-established biology; the mechanism is understood and uncontested | The link is consistent with known biology but the mechanism is partly inferred | Only a general argument that the link is possible; intervening steps are assumed |
| **Empirical support** | Multiple independent studies, ideally including human data, with dose or time concordance | Several studies, or one strong study, with some inconsistency or only model systems | Few studies, indirect measurements, or inference from a related system |
| **Quantitative understanding** | The relationship can be modelled: thresholds or dose-response are characterised | Direction and rough magnitude are known; no usable model | Direction only |

**Mechanistic plausibility alone is `empirical_support: low`, not `moderate`.** If no
study measured the two events and related them, the support is low however convincing the
mechanism. This is where a resource about beneficial effects is most prone to optimism,
so it is the rating to be strictest about.

Every relationship needs at least one reference with a DOI or a PMID. Say in the page
body what *kind* of evidence it is — human randomised trial, cohort, animal, in vitro,
in silico — because the grade alone does not carry that.

Then, on the pathway that uses the link, record `essentiality` (how much the pathway
depends on this step) and `confidence` (how sure you are of it *in this pathway*). Those
are context judgements and belong to the pathway, not the relationship.

### Three mistakes the validator will catch

**Quote a CURIE if it has a space after the colon.** `- MONDO: 0013209` is read by YAML
as the mapping `{MONDO: 13209}` and the leading zeros are gone. Written without the
space, `- MONDO:0013209` is a plain string and is fine — but quoting everything
(`"MONDO:0013209"`) is the habit that never bites.

**Quote a bare zero-padded number.** `identifier: 0001` becomes the integer `1`. With its prefix,
`identifier: "BOPE:0001"` is a string and keeps its padding. Always write the prefix.

**The key is `identifier:`, never `id:`.** Jekyll's own `Document#id` shadows a
front-matter `id` and returns the document's path instead, so every template lookup
silently resolves to nothing and pages render "(no page)" with no error anywhere. The
schema rejects `id:` outright so this cannot happen quietly.

**Never put `role:` on an event page.** Role is the part an event plays in one pathway,
and goes in that pathway's `events:` list. The same event plays a different part
elsewhere.

### Check it before you open the pull request

```bash
pip install -r tools/requirements.txt
python tools/validate.py
```

Beyond the schema, this checks that filenames match identifiers, that identifiers are
unique, that every referenced event and relationship resolves, that a relationship's two
endpoints are both in the pathway citing it, that the edges form an acyclic graph with an
initiating event and an outcome, and that every ontology prefix is either known or backed
by a term page.

**Note on cycles.** The graph must be acyclic, which the grammar inherited from AOPs
requires. Real biology has feedback loops; describe them in the page body, as
[BOP:1](_bops/BOP-1.md) does, rather than trying to encode one as an edge.

To see the pages, no Ruby needed:

```bash
docker run --rm -u "$(id -u):$(id -g)" -v "$PWD":/app -w /app -p 4000:4000 \
  -e BUNDLE_PATH=/app/vendor/bundle -e HOME=/tmp ruby:3.3 \
  bash -lc "bundle install && bundle exec jekyll serve --host 0.0.0.0"
```

## Writing the prose

The front matter is the data; the body is where you say what the data cannot.

Write for a reader who knows the biology but not this pathway. Explain *why* a grade is
what it is, especially when it is low — "empirical support is low because the only
evidence is X" is worth more than the word "low" on its own. Name the weakest link
explicitly; a pathway that admits where it is thin is more useful and more credible than
one that does not.

Do not copy descriptive text from AOP-Wiki. Its content is CC BY-SA 4.0, and this
repository is CC0; pulling its prose in would drag an incompatible licence with it.
Cross-reference its identifiers freely and write your own descriptions.

## Review

A maintainer checks that the validator passes, that the evidence grades match what the
cited papers actually show, that reuse was attempted before new events were minted, and
that the prose explains the grades. Expect a first response within about two weeks.

Everything starts at `status: draft`. Promotion to `under-review` and then `endorsed`
needs a curator other than the author. There is no automatic promotion.

By contributing you agree to release curated content under
[CC0 1.0](LICENSE-CONTENT) and code under the [MIT licence](LICENSE), and to follow the
[code of conduct](CODE_OF_CONDUCT.md).
