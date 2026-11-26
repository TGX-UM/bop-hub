---
layout: default
title: Relationships
permalink: /browse/relationships/
description: Every causal link in BOP-Hub, with its intrinsic weight of evidence.
---

<h1>Relationships</h1>

<p class="lede">Each relationship is one causal link between two events, with the
evidence for the link itself. Pathways reuse these links and add their own judgement of
how essential each is.</p>

<div class="table-scroll">
<table>
  <thead>
    <tr>
      <th scope="col">Relationship</th>
      <th scope="col">Adjacency</th>
      <th scope="col">Biological<br>plausibility</th>
      <th scope="col">Empirical<br>support</th>
      <th scope="col">Quantitative<br>understanding</th>
      <th scope="col" class="num">BOPs</th>
    </tr>
  </thead>
  <tbody>
  {%- for r in site.relationships %}
    {%- assign uses = 0 %}
    {%- for bop in site.bops %}{% for item in bop.relationships %}{% if item.ker == r.identifier %}{% assign uses = uses | plus: 1 %}{% endif %}{% endfor %}{% endfor %}
    <tr>
      <td><a href="{{ r.url | relative_url }}">{{ r.title }}</a><br><span class="ident">{{ r.identifier }}</span></td>
      <td>{{ r.adjacency }}</td>
      <td>{% include evidence.html grade=r.evidence.biological_plausibility %}</td>
      <td>{% include evidence.html grade=r.evidence.empirical_support %}</td>
      <td>{% include evidence.html grade=r.evidence.quantitative_understanding %}</td>
      <td class="num">{{ uses }}</td>
    </tr>
  {%- endfor %}
  </tbody>
</table>
</div>
