---
layout: default
title: BOPs
permalink: /browse/bops/
description: Every beneficial outcome pathway curated in BOP-Hub.
---

<h1>Beneficial outcome pathways</h1>

<p class="lede">Every beneficial outcome pathway curated here, with the number of events
and links it assembles and the overall confidence placed in it.</p>

<div class="table-scroll">
<table>
  <thead>
    <tr>
      <th scope="col">BOP</th>
      <th scope="col">Beneficial outcome</th>
      <th scope="col">Status</th>
      <th scope="col" class="num">Events</th>
      <th scope="col" class="num">Links</th>
      <th scope="col">Confidence</th>
    </tr>
  </thead>
  <tbody>
  {%- for bop in site.bops %}
    {%- assign outcome_id = "" %}
    {%- for item in bop.events %}{% if item.role == "outcome" %}{% assign outcome_id = item.event %}{% endif %}{% endfor %}
    {%- assign outcome = site.events | where: "identifier", outcome_id | first %}
    <tr>
      <td><a href="{{ bop.url | relative_url }}">{{ bop.short_title | default: bop.title }}</a>
        <br><span class="ident">{{ bop.identifier }}</span></td>
      <td>{% if outcome %}<a href="{{ outcome.url | relative_url }}">{{ outcome.title }}</a>{% else %}—{% endif %}</td>
      <td><span class="status">{{ bop.status }}</span></td>
      <td class="num">{{ bop.events | size }}</td>
      <td class="num">{{ bop.relationships | size }}</td>
      <td>{% include evidence.html grade=bop.overall_confidence %}</td>
    </tr>
  {%- endfor %}
  </tbody>
</table>
</div>

{%- if site.bops.size == 0 %}
<p>No pathways yet.</p>
{%- endif %}
