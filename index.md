---
layout: home
title: BOP-Hub
description: A community-curated knowledge base of Beneficial Outcome Pathways, the beneficial counterpart to AOP-Wiki.
---

<h1>Beneficial Outcome Pathways</h1>

<p class="lede">A beneficial outcome pathway records how a beneficial exposure or
intervention leads, step by measurable step, to a health benefit — and how good the
evidence is for each step. BOP-Hub curates them in the same grammar that
<a href="https://aopwiki.org/">AOP-Wiki</a> uses for harm, so the two can be read
together.</p>

{%- assign bop = site.bops | sort: "id" | first %}
{%- if bop %}
<h2>The pathway curated so far</h2>

<p><a href="{{ bop.url | relative_url }}"><strong>{{ bop.title }}</strong></a><br>
<span class="ident">{{ bop.identifier }} · {{ bop.events | size }} events · {{ bop.relationships | size }} relationships · overall confidence {{ bop.overall_confidence }}</span></p>

<div class="table-scroll">
<table>
  <caption>Every event in {{ bop.identifier }}, in the order it is recorded. Follow a link to read the evidence for that step.</caption>
  <thead><tr><th scope="col">Role</th><th scope="col">Event</th><th scope="col">Level</th></tr></thead>
  <tbody>
  {%- for item in bop.events %}
    {%- assign ev = site.events | where: "identifier", item.event | first %}
    <tr class="ev-row is-{{ item.role }}">
      <td><span class="role role-{{ item.role }}">{{ item.role }}</span></td>
      <td><a href="{{ ev.url | relative_url }}">{{ ev.title }}</a></td>
      <td>{{ ev.biological_level }}</td>
    </tr>
  {%- endfor %}
  </tbody>
</table>
</div>
{%- endif %}

<h2>What is in here</h2>

<dl class="counts">
  <div><dt>Pathways</dt><dd>{{ site.bops | size }}</dd></div>
  <div><dt>Events</dt><dd>{{ site.events | size }}</dd></div>
  <div><dt>Relationships</dt><dd>{{ site.relationships | size }}</dd></div>
  <div><dt>Ontology terms</dt><dd>{{ site.annotations | size }}</dd></div>
</dl>

<div class="caveat">
  <p><strong>Version 0. The schema is not yet stable.</strong> Expect breaking changes
  to the content model before 1.0. Identifiers, once issued, will not be reused or
  renumbered.</p>
  <p><strong>Nothing here is medical advice.</strong> BOP-Hub maps mechanisms and the
  evidence behind them. It does not recommend treatments, authorise health claims, or
  substitute for regulatory assessment.</p>
</div>

<h2>How it is put together</h2>

<div class="prose">
<p>Four kinds of page, and one rule that makes them worth separating.</p>

<ul>
  <li>A <strong>pathway</strong> assembles events into a causal chain and rates how
  essential each link is to that chain.</li>
  <li>An <strong>event</strong> is a measurable biological change. Events are reusable:
  the same event can appear in many pathways.</li>
  <li>A <strong>relationship</strong> is a causal link between two events, carrying the
  evidence for the link itself.</li>
  <li>A <strong>term</strong> is an ontology concept used to say where a pathway applies.</li>
</ul>

<p>The rule: the part an event plays — the trigger, a step along the way, or the
outcome — belongs to the pathway, not to the event. Improved insulin sensitivity is
the endpoint of one pathway and a step on the way to another. Recording the part on
the event page would make that impossible, and it is why events can be shared at all.</p>

<p>The same reasoning applies across frameworks. An event that is beneficial here may
be the adverse direction of an event already in AOP-Wiki; where that is so, both are
recorded, and kept distinct.</p>
</div>

<h2>Contribute</h2>

<div class="prose">
<p>You do not need to know Jekyll, or write any YAML, to add a pathway.
<a href="https://github.com/{{ site.github_username }}/{{ site.github_repo }}/issues/new/choose">Open
an issue describing the pathway and its evidence</a>, and a maintainer will write it up
with you. If you would rather do it yourself, <a href="{{ '/contribute/' | relative_url }}">the
contributor guide</a> walks through adding one from start to finish.</p>
</div>
