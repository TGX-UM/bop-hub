---
layout: default
title: About
permalink: /about/
description: What BOP-Hub is for, what it is not for, and who maintains it.
---

<h1>About BOP-Hub</h1>

<div class="prose">

<p class="lede">BOP-Hub is a community-curated knowledge base of beneficial outcome
pathways: causal chains linking a beneficial exposure or intervention, through
measurable key events, to a benefit to health.</p>

<h2>Where the idea comes from</h2>

<p>Adverse outcome pathways were developed in regulatory toxicology to organise what is
known about how a chemical causes harm, as a sequence of key events from a molecular
initiating event to an adverse outcome, with the evidence for each causal link graded
explicitly. The approach let regulators reason about chemicals it would be unethical to
test on people, and reduced reliance on animal testing.</p>

<p>Beneficial outcome pathways carry that grammar over to interventions meant to do
good: a nutrient, a dietary pattern, a fasting regimen, exercise. The motivation is a
real methodological problem. Lifestyle interventions often cannot be tested in
placebo-controlled randomised trials, so their evidence base ends up fragmented and
heterogeneous, and reads as weaker than it is. Structuring the mechanism makes it
possible for a small study to test one link in a chain rather than needing to
demonstrate a long-term clinical outcome on its own.</p>

<p>The framework was introduced by Robin Mesnage and Verena Buchinger in 2026, who
applied it to fasting in metabolic dysfunction-associated steatotic liver disease
(<a href="https://doi.org/10.1155/jnme/3190642">doi:10.1155/jnme/3190642</a>). That
pathway is curated here as <a href="{{ '/bops/BOP-1/' | relative_url }}">BOP:1</a>.</p>

<h2>What this resource is for</h2>

<ul>
  <li>Structuring a mechanistic hypothesis so that its parts can be tested separately.</li>
  <li>Mapping where the evidence for an intervention is strong and where it is thin.</li>
  <li>Anchoring omics and other new-approach-methodology data to specific events.</li>
  <li>Reading beneficial and adverse pathways against each other, where they share events.</li>
</ul>

<h2>What it is not for</h2>

<p>This matters more here than it would for a resource about harm, because a collection
of pathways about the benefits of diets and supplements invites misreading, in good
faith and otherwise.</p>

<ul>
  <li><strong>It is not medical advice</strong>, and no page should be read as a
  recommendation to undertake any intervention.</li>
  <li><strong>It does not authorise health claims.</strong> A pathway recorded here
  carries no regulatory status whatever.</li>
  <li><strong>It does not substitute for regulatory assessment</strong> by EFSA or any
  other authority.</li>
  <li><strong>It is not a clinical guideline</strong>, and it is not evidence that an
  intervention is safe. Several pathways here describe interventions that are harmful to
  some people; where that is known, the pathway page says so.</li>
</ul>

<p>A pathway asserts that an intervention <em>can plausibly</em> lead to an outcome in
at least some people, with the strength of the evidence stated. It does not assert that
it will, or that it is advisable.</p>

<h2>How evidence is graded</h2>

<p>Each causal link is graded on three dimensions adapted from the modified
Bradford-Hill considerations used for adverse outcome pathways: biological plausibility,
empirical support, and quantitative understanding. Each is rated high, moderate or low.
A pathway that uses a link additionally records how essential that link is to it, and
its confidence in the link in that particular context, because the same causal step can
be load-bearing in one pathway and incidental in another.</p>

<p>Grades are shown as filled bars next to their own word, never as colours. Colour on
this site means the part an event plays, and a green "high" would read as an
endorsement of the intervention rather than a statement about evidence.</p>

<h2>Status and governance</h2>

<p>This is version 0. One pathway is curated, the schema is not yet stable, and
breaking changes should be expected before 1.0. Identifiers are the exception: once
issued, they are never reused or renumbered.</p>

<p>Pathways carry a curation status of draft, under review, or endorsed. Everything is
currently draft. Promotion beyond draft requires review by a curator other than the
author. BOP-Hub is maintained at the Department of Translational Genomics, Maastricht
University, and changes arrive as pull requests, each one reviewed by a maintainer and
checked automatically against the content schema.</p>

<h2>Reuse</h2>

<p>Curated content is released under
<a href="https://creativecommons.org/publicdomain/zero/1.0/">CC0 1.0</a>: use it without
restriction and without needing to ask. The site code is MIT, and its scaffolding derives
from the <a href="https://github.com/wikipathways/Jiffy">Jiffy</a> template by the
WikiPathways team. A machine-readable dump of the content is at
<a href="{{ '/api/bops.json' | relative_url }}">/api/bops.json</a> and
<a href="{{ '/api/events.json' | relative_url }}">/api/events.json</a>.</p>

</div>
