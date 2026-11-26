---
layout: default
title: Events
permalink: /browse/events/
description: Every event in BOP-Hub, grouped by level of biological organisation.
---

<h1>Events</h1>

<p class="lede">Events are reusable: one event can appear in many pathways, playing a
different part in each. They are grouped here by level of biological organisation, from
molecules up to populations.</p>

{%- assign order = "molecular,cellular,tissue,organ,individual,population" | split: "," %}
{%- for level in order %}
  {%- assign group = site.events | where: "biological_level", level %}
  {%- if group.size > 0 %}
<h2>{{ level | capitalize }} <span class="ident">{{ group.size }}</span></h2>
<div class="table-scroll">
<table>
  <thead><tr><th scope="col">Event</th><th scope="col">Process term</th><th scope="col">In AOP-Wiki</th><th scope="col" class="num">Pathways</th></tr></thead>
  <tbody>
  {%- for ev in group %}
    {%- assign uses = 0 %}
    {%- for bop in site.bops %}{% for item in bop.events %}{% if item.event == ev.identifier %}{% assign uses = uses | plus: 1 %}{% endif %}{% endfor %}{% endfor %}
    <tr>
      <td><a href="{{ ev.url | relative_url }}">{{ ev.title }}</a><br><span class="ident">{{ ev.identifier }}</span></td>
      <td>{% if ev.process %}<span class="mono">{{ ev.process }}</span>{% else %}<span class="ev-word">not assigned</span>{% endif %}</td>
      <td>
        {%- if ev.aopwiki_ke -%}
          {%- assign ke = ev.aopwiki_ke | remove: "aop.events:" -%}
          <a href="https://aopwiki.org/events/{{ ke }}">KE {{ ke }}</a>
        {%- elsif ev.aopwiki_mirror_ke -%}
          {%- assign mk = ev.aopwiki_mirror_ke | remove: "aop.events:" -%}
          <span class="ev-word">mirror of</span> <a href="https://aopwiki.org/events/{{ mk }}">KE {{ mk }}</a>
        {%- else -%}
          <span class="ev-word">—</span>
        {%- endif -%}
      </td>
      <td class="num">{{ uses }}</td>
    </tr>
  {%- endfor %}
  </tbody>
</table>
</div>
  {%- endif %}
{%- endfor %}
