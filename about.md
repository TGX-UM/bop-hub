---
layout: default
title: About
permalink: /about/
description: What BOP-Hub is for, what it is not for, and who maintains it.
---

<h1>About BOP-Hub</h1>

<div class="prose">

<p class="lede">BOP-Hub is a community-curated knowledge base of beneficial outcome
pathways: causal chains linking an intervention, through measurable key events, to a
benefit to health.</p>

<h2>Where the idea comes from</h2>

<p>Adverse outcome pathways came out of regulatory toxicology. They organise what is known
about how a chemical causes harm as a sequence of key events, from a molecular initiating
event to an adverse outcome, with the evidence for each causal link graded openly. That
let regulators reason about chemicals nobody could ethically test on people, and it cut
down on animal testing.</p>

<p>Beneficial outcome pathways carry the same grammar over to things meant to do good: a
nutrient, a dietary pattern, a fasting regimen, exercise. The motivation is a real
methodological problem. You usually cannot run a placebo-controlled trial of a lifestyle
intervention, so the evidence ends up scattered across small heterogeneous studies and
reads as weaker than it is. Writing down the mechanism lets one study test one link in the
chain instead of having to carry a long-term clinical outcome by itself.</p>

<p>Robin Mesnage and Verena Buchinger introduced the framework in 2026 and applied it to
fasting in metabolic dysfunction-associated steatotic liver disease
(<a href="https://doi.org/10.1155/jnme/3190642">doi:10.1155/jnme/3190642</a>). That
pathway is curated here as <a href="{{ '/bops/BOP-1/' | relative_url }}">BOP:1</a>.</p>

<h2>What this is for</h2>

<p>Mainly, structuring a mechanistic hypothesis so its parts can be tested one at a time,
and mapping where the evidence for an intervention is solid and where it is thin. It is
also somewhere to anchor omics and other new-approach-methodology data to specific events,
and a way to read beneficial and adverse pathways against each other where they share
events.</p>

<h2>What it is not for</h2>

<p>This matters more here than it would for a resource about harm. A collection of
pathways about the benefits of diets and supplements invites misreading, some of it in
good faith and some of it not.</p>

<p>Nothing on this site is medical advice, and no page should be read as a recommendation
to try anything. A BOP recorded here carries no regulatory standing, authorises no health
claim, and replaces no assessment by EFSA or any other authority. It is also not evidence
that an intervention is safe. Several pathways here describe interventions that harm some
people, and where that is known the page says so.</p>

<p>What a BOP does claim is narrow: that an intervention <em>can plausibly</em> lead to an
outcome in at least some people, with the strength of the evidence stated. Not that it
will, and not that anyone should try it.</p>

<h2>How evidence is graded</h2>

<p>Each causal link is graded on three dimensions adapted from the modified Bradford-Hill
considerations used for adverse outcome pathways: biological plausibility, empirical
support, and quantitative understanding. Each is rated high, moderate or low. A BOP that
uses a link then records how much it depends on that link, and how confident it is in the
link in that particular context, because the same causal step can be load-bearing in one
pathway and incidental in another.</p>

<p>Grades show up as filled bars beside the word, never as colour. Colour on this site
means the part an event plays. A green "high" would read as approval of the intervention
rather than a statement about evidence, and that is the confusion this resource can least
afford.</p>

<h2>Status and governance</h2>

<p>This is version 0. One pathway is curated, the schema is not stable, and it will change
in ways that break things before 1.0. Identifiers are the exception: once issued, one is
never reused and never renumbered.</p>

<p>Pathways carry a curation status of draft, under review, or endorsed. Everything is
currently draft. Getting past draft needs a curator other than the author to look at it.
BOP-Hub is maintained at the Department of Translational Genomics, Maastricht University.
Changes arrive as pull requests, each reviewed by a maintainer and checked automatically
against the content schema.</p>

<h2>Reuse</h2>

<p>Curated content is released under
<a href="https://creativecommons.org/publicdomain/zero/1.0/">CC0 1.0</a>, so use it however
you like without asking. The site code is MIT, and its scaffolding derives from the
<a href="https://github.com/wikipathways/Jiffy">Jiffy</a> template by the WikiPathways
team. Every record, including the prose below each page's front matter, is published as
JSON at <a href="{{ '/api/' | relative_url }}">/api/</a> — the whole graph is about 13 KB
gzipped, so it is meant to be downloaded and queried in one piece.</p>

</div>
