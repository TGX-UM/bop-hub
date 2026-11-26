---
layout: default
title: Contribute
permalink: /contribute/
description: How to add a beneficial outcome pathway to BOP-Hub. No Jekyll or YAML needed.
---

<h1>Contribute a BOP</h1>

<div class="prose">

<p class="lede">You do not need to know Jekyll, or write a line of YAML, to add a pathway
here. Describing it is enough. A maintainer turns your description into the files and
credits you as its curator.</p>

<h2>Three ways in, easiest first</h2>

<h3>Describe it and let a maintainer write it up</h3>

<p>This is the route we expect domain experts to take, not a fallback.
<a href="https://github.com/{{ site.github_username }}/{{ site.github_repo }}/issues/new?template=propose-pathway.yml">Open
a proposal</a> and tell us the intervention, the chain of events, the outcome, and the
papers behind each step. Gaps are fine. We will work through them with you.</p>

<h3>Fix a page in the browser</h3>

<p>Every page has an "Edit this page on GitHub" link at the bottom. Use it for a typo, a
clarification, an added reference. GitHub handles the fork and the pull request.</p>

<h3>Fork and curate</h3>

<p>Full control over the files.
<a href="https://github.com/{{ site.github_username }}/{{ site.github_repo }}/blob/main/CONTRIBUTING.md">The
contributor guide</a> walks through adding a BOP from identifier allocation to opening the
pull request, and spells out the evidence rubric.</p>

<h2>Two things worth knowing first</h2>

<h3>Look for the event before you mint a new one</h3>

<p>Search the <a href="{{ '/browse/events/' | relative_url }}">events already here</a>, then
search <a href="https://aopwiki.org/events">AOP-Wiki</a>. If the event exists there in the
same direction, reuse its identifier. If AOP-Wiki has the opposite direction, the same
thing measured going the other way, that is a <em>different</em> event and gets recorded
as a mirror rather than a match.</p>

<p>This is what decides whether BOP-Hub ends up connected to anything. An event shared
with an AOP is what lets someone ask where a beneficial and an adverse pathway meet.</p>

<h3>Be strict about empirical support</h3>

<p>Each causal link is graded on biological plausibility, empirical support and
quantitative understanding. The second one is where people go wrong.</p>

<p><strong>A convincing mechanism with no study that measured both events is
<code>low</code> empirical support, not <code>moderate</code>.</strong> This is where a
resource about beneficial effects slides into optimism, and being blunt about it is what
makes the other grades worth anything. A pathway that says plainly where it is thin is
more useful than one that does not, and a good deal more credible.</p>

<h2>What happens next</h2>

<p>A maintainer checks that the validator passes, that the grades match what the cited
papers actually show, that you looked for an existing event first, and that the prose
explains the grades. Expect a first response within a fortnight or so.</p>

<p>Everything starts as a draft. Getting past draft needs a curator other than the author;
nothing is promoted automatically. Curated content goes out under
<a href="https://creativecommons.org/publicdomain/zero/1.0/">CC0 1.0</a>, so anyone can
reuse it without asking.</p>

</div>
