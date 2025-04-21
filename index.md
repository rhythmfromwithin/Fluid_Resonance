---
layout: default
title: Rhythm from within
---
# 欢迎来我的写作空间小坐

这是我的说给宇宙听系列文字。

## 文档目录

{% for file in site.static_files %}
  {% if file.extname == '.md' and file.name != 'index.md' and file.name != 'README.md' %}
  - [{{ file.name | remove: '.md' }}]({{ file.path }})
  {% endif %}
{% endfor %}
