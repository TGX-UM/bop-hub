---
layout: default
title: Terms
permalink: /browse/annotations/
description: The ontology terms used to record where a pathway applies.
---

<h1>Ontology terms</h1>

<p class="lede">The terms used to state where a pathway applies: which intervention,
which species, which sex, which life stage, which disease and which phenotype. Grouped
by the slot they fill.</p>

{%- for slot in site.annotation_slots %}
  {%- assign group = site.annotations | where_exp: "a", "a.slot contains slot" %}
  {%- if group.size > 0 %}
<h2>{{ slot | replace: "_", " " | capitalize }}</h2>
<ul class="chips">
  {%- for term in group %}
  <li><a class="chip" href="{{ term.url | relative_url }}">{{ term.label }}<span class="ident">{{ term.identifier }}</span></a></li>
  {%- endfor %}
</ul>
  {%- endif %}
{%- endfor %}
