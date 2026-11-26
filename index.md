---
layout: home
title: BOP-Hub
description: A community-curated knowledge base of Beneficial Outcome Pathways, the beneficial counterpart to AOP-Wiki.
---

<h1>Beneficial Outcome Pathways</h1>

<p class="lede">A beneficial outcome pathway sets out how an intervention leads to a
health benefit, one measurable step at a time, and says how good the evidence is for each
step. BOP-Hub curates them in the grammar <a href="https://aopwiki.org/">AOP-Wiki</a>
uses for harm, so you can read the two against each other.</p>

{%- assign bop = site.bops | sort: "identifier" | first %}
{%- if bop %}
<h2>The BOP curated so far</h2>

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
  <div><dt>BOPs</dt><dd>{{ site.bops | size }}</dd></div>
  <div><dt>Events</dt><dd>{{ site.events | size }}</dd></div>
  <div><dt>Relationships</dt><dd>{{ site.relationships | size }}</dd></div>
  <div><dt>Ontology terms</dt><dd>{{ site.annotations | size }}</dd></div>
</dl>

<div class="caveat">
  <p><strong>Version 0. The schema is not stable yet.</strong> Expect it to change in ways
  that break things before 1.0. Identifiers are the exception: once issued, one is never
  reused and never renumbered.</p>
  <p><strong>Nothing here is medical advice.</strong> BOP-Hub maps mechanisms and the
  evidence behind them. It does not tell anyone what to eat or what to take, and a BOP
  carries no regulatory standing of any kind.</p>
</div>

<h2>How it is put together</h2>

<div class="prose">
<p>Four kinds of page. A <strong>BOP</strong> assembles events into a causal chain and
rates how much the chain depends on each link. An <strong>event</strong> is a measurable
biological change, and the same event can turn up in many BOPs. A
<strong>relationship</strong> is a causal link between two events, carrying the evidence
for that link. A <strong>term</strong> is an ontology concept that says where a BOP
applies.</p>

<p>One rule holds the whole thing together: the part an event plays belongs to the BOP,
not to the event. Improved insulin sensitivity is where one BOP ends and a waypoint in
another. Pin the part to the event page and that becomes impossible, which is the reason
events can be shared at all.</p>

<p>The same logic reaches across to AOP-Wiki. An event that is beneficial here may be the
adverse direction of one already recorded there. Both get written down, and they are kept
apart.</p>
</div>

<h2>Contribute</h2>

<div class="prose">
<p>You do not need to know Jekyll, or write a line of YAML, to add a BOP.
<a href="https://github.com/{{ site.github_username }}/{{ site.github_repo }}/issues/new/choose">Open
an issue describing the pathway and its evidence</a> and a maintainer will write it up with
you. If you would rather do it yourself,
<a href="{{ '/contribute/' | relative_url }}">the contributor guide</a> goes through adding
one from start to finish.</p>
</div>
