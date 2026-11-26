---
layout: default
title: Contribute
permalink: /contribute/
description: How to add a beneficial outcome pathway to BOP-Hub. No Jekyll or YAML needed.
---

<h1>Contribute a pathway</h1>

<div class="prose">

<p class="lede">You do not need to know Jekyll, or write any YAML, to add a pathway here.
Describing it is enough — a maintainer will turn your description into the files and
credit you as its curator.</p>

<h2>Three ways in, easiest first</h2>

<h3>Describe it and let a maintainer write it up</h3>

<p>This is the expected route for domain experts, not a fallback.
<a href="https://github.com/{{ site.github_username }}/{{ site.github_repo }}/issues/new?template=propose-pathway.yml">Open
a pathway proposal</a> and tell us the intervention, the chain of events, the outcome,
and the papers behind each step. Gaps are fine; we will work through them with you.</p>

<h3>Fix a page in the browser</h3>

<p>Every page has an "Edit this page on GitHub" link at the bottom. Use it for a typo, a
clarification or an added reference — GitHub handles the fork and the pull request.</p>

<h3>Fork and curate</h3>

<p>Full control over the files.
<a href="https://github.com/{{ site.github_username }}/{{ site.github_repo }}/blob/main/CONTRIBUTING.md">The
contributor guide</a> walks through adding a pathway from identifier allocation to
opening the pull request, and documents the evidence rubric in full.</p>

<h2>Two things worth knowing before you start</h2>

<h3>Reuse an event before minting a new one</h3>

<p>Search the <a href="{{ '/browse/events/' | relative_url }}">existing events</a>, and
then <a href="https://aopwiki.org/events">AOP-Wiki</a>. If the event is already there in
the same direction, reuse its identifier. If AOP-Wiki has the opposite direction — the
same thing measured, going the other way — that is a <em>different</em> event, and it is
recorded as a mirror rather than a match.</p>

<p>This is the rule that decides whether BOP-Hub is interoperable or an island. An event
shared with an AOP is what lets someone ask where a beneficial and an adverse pathway
meet.</p>

<h3>Be strict about empirical support</h3>

<p>Each causal link is graded on biological plausibility, empirical support and
quantitative understanding. The rating people get wrong is the second one.</p>

<p><strong>A convincing mechanism with no study that measured both events is
<code>low</code> empirical support, not <code>moderate</code>.</strong> This is where a
resource about beneficial effects is most prone to optimism, and being honest about it is
what makes the rest of the grades worth reading. A pathway that says plainly where it is
thin is more useful, and more credible, than one that does not.</p>

<h2>What happens to your contribution</h2>

<p>A maintainer checks that the validator passes, that the grades match what the cited
papers show, that reuse was attempted, and that the prose explains the grades. Expect a
first response within about two weeks.</p>

<p>Everything starts as a draft. Promotion beyond draft requires review by a curator
other than the author — there is no automatic promotion. Curated content is released
under <a href="https://creativecommons.org/publicdomain/zero/1.0/">CC0 1.0</a>, so
anyone can reuse it without asking.</p>

</div>
