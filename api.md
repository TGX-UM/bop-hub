---
layout: default
title: API
permalink: /api/
description: "The machine-readable view of BOP-Hub: every record, every schema, and the fixity manifest."
---

<h1>API</h1>

<p class="lede">BOP-Hub is a git repository, and this is its published,
machine-readable view. Everything under <code>/api/v1/</code> is generated from
the same records the site renders and the same rules the validator enforces, so
it cannot disagree with either.</p>

<h2>The whole thing</h2>

<p>The complete graph is about 13 KB gzipped, including every Markdown body, so
the usual way to use this API is to download it once and query it in memory. You
do not need a query engine, and there is no rate limit to respect.</p>

<ul>
  <li><a href="{{ '/api/v1/graph.json' | relative_url }}"><code>/api/v1/graph.json</code></a>
      — all four collections in one document</li>
  <li><a href="{{ '/api/v1/index.json' | relative_url }}"><code>/api/v1/index.json</code></a>
      — counts, the commit this was built from, the next free identifiers, and the content digest</li>
</ul>

<h2>Per collection, per record</h2>

<ul>
  <li><code>/api/v1/bops.json</code>, <code>/api/v1/events.json</code>,
      <code>/api/v1/relationships.json</code>, <code>/api/v1/annotations.json</code></li>
  <li><code>/api/v1/bops/BOP-1.json</code>, <code>/api/v1/events/BOPE-0001.json</code>,
      and so on — the file name is the identifier with its colon replaced, exactly as in the
      repository and in the page URL</li>
</ul>

<h2>What a record carries</h2>

<p>Every field of the page's front matter, plus four computed ones:</p>

<dl>
  <dt><code>page_iri</code></dt>
  <dd>This record's canonical BOP-Hub IRI, under
      <code>{{ site.canonical_base }}</code>. It is computed from the permalink and never
      stored in a page, so moving the site does not invalidate one.</dd>
  <dt><code>iri</code></dt>
  <dd>The same thing for a BOP, event or relationship. On an annotation it is instead the
      ontology term's own PURL, because that page is <em>about</em> that term.</dd>
  <dt><code>url</code></dt>
  <dd>Where the human-readable page is served right now. Unlike the IRI, this changes if
      the site moves.</dd>
  <dt><code>body_markdown</code></dt>
  <dd>The prose below the front matter, verbatim. On a BOP that is the weight-of-evidence
      discussion and the safety section; on a relationship it is what a
      <code>description</code> field would otherwise hold. It is curated content that
      exists nowhere else, and it is not in the older dumps.</dd>
</dl>

<p>A BOP's <code>events</code> and <code>relationships</code> entries each carry a
<code>position</code>, which is their order in the pathway as curated. That order is
rendered on the BOP page and is not recoverable from the graph: the pathway branches, so
a topological sort is not unique. Each cited relationship also has its
<code>upstream_event</code>, <code>downstream_event</code> and <code>adjacency</code>
joined in, so the edge list needs no second lookup.</p>

<p>Note where the evidence lives, because it is two-layer by design. A relationship record
carries the <em>intrinsic</em> grades in <code>evidence</code>. The
<code>essentiality</code> and <code>confidence</code> of that same relationship
<em>within a given BOP</em> are on the BOP's own entry for it, because a step can be
load-bearing in one pathway and incidental in another. For the same reason
<code>role</code> is on a BOP's event entry and never on the event itself.</p>

<h2>The rules, as actually enforced</h2>

<p><code>/api/v1/schema/{bop,event,relationship,annotation}.json</code> are the normative
schemas with their <code>$ref</code>s inlined and their controlled vocabularies expanded
into <code>enum</code>s — the same objects the exporter validated against.
<code>/api/v1/vocab.json</code> is the vocabularies on their own.</p>

<p>If you validate in a browser with Ajv, add <code>ajv-formats</code>: without it
<code>"format": "date"</code> is ignored and a malformed date passes.</p>

<h2>Fixity</h2>

<p><code>/api/v1/manifest.json</code> gives a SHA-256 for every file plus a
<code>content_digest</code> over all of them. The digest covers content only —
<code>generated</code> appears in <code>index.json</code> and nowhere else — so two builds
of the same commit produce the same digest, and a changed digest means the content changed.</p>

<h2>Still served</h2>

<p><a href="{{ '/api/bops.json' | relative_url }}"><code>/api/bops.json</code></a> and
<a href="{{ '/api/events.json' | relative_url }}"><code>/api/events.json</code></a> predate
this API and continue to work unchanged. They carry a narrower set of fields and no bodies.
The build fails if they and <code>/api/v1/</code> ever disagree about a field they share.</p>

<h2>Licence</h2>

<p>Content is CC0-1.0: reuse it freely, no attribution required, though citing us helps —
see <a href="https://github.com/{{ site.repository }}/blob/main/CITATION.cff">CITATION.cff</a>.
Identifiers of other resources appear here as cross-references; AOP-Wiki's own content is
CC BY-SA 4.0 and is not reproduced.</p>
