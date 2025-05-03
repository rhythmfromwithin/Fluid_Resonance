---
layout: page
title: Archive
permalink: /archive/
---

<h1>所有文章</h1>

{% for collection in site.collections %}
  {% if collection.label != "posts" %}
    <h2>{{ collection.title | default: collection.label }}</h2>
    <ul>
    {% for post in site[collection.label] %}
      <li>
        <span class="post-date">{{ post.date | date: site.minima.date_format }}</span>
        <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
        {% if post.subtitle %} - {{ post.subtitle }}{% endif %}
      </li>
    {% endfor %}
    </ul>
  {% endif %}
{% endfor %}