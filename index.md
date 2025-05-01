---
layout: home
title: Rhythm from within
---
# 欢迎来我的写作空间小坐

这是我的说给宇宙听系列文字。

我以前认为创作是一件危险的事情  

现在我不这样认为了  

但是  

我始终觉得  

人要有敬畏之心  


我们老家有句老话是  

举头三尺有神明  


我觉得写的时候  

人要对自己诚实  

非说不可的才要写下来  

其他的都是随缘了  

我给自己写的东西取名叫  

把话说给宇宙听系列  

其实也是对无以名状之物的敬畏  


## 文档目录

{% for file in site.static_files %}
  {% if file.extname == '.md' and file.name != 'index.md' and file.name != 'README.md' %}
  - [{{ file.name | remove: '.md' }}]({{ file.path }})
  {% endif %}
{% endfor %}

