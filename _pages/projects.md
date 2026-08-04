---
layout: page
title: Projects
permalink: /projects/
description: Selected healthcare data science, machine learning, and applied AI projects.
nav: true
nav_order: 3
display_categories:
horizontal: false
---

<link rel="stylesheet" href="{{ '/assets/css/marcin.css' | relative_url }}">

<section class="projects-intro">
  <h2>Project Portfolio</h2>
  <p>
    A focused set of healthcare analytics, applied machine learning, and LLM engineering projects. I try to show the full workflow behind each project: problem framing, data pipeline, modeling or agent design, validation, limitations, and the practical value for a real user.
  </p>
  <div class="hero-actions">
    <a class="site-button primary" href="{{ '/projects/healthcare_operations_copilot/' | relative_url }}">Featured AI Agent</a>
    <a class="site-button" href="{{ '/cv/' | relative_url }}">Resume</a>
  </div>
</section>

<!-- pages/projects.md -->
<div class="projects">
{% if site.enable_project_categories and page.display_categories %}
  <!-- Display categorized projects -->
  {% for category in page.display_categories %}
  <a id="{{ category }}" href=".#{{ category }}">
    <h2 class="category">{{ category }}</h2>
  </a>
  {% assign categorized_projects = site.projects | where: "category", category %}
  {% assign sorted_projects = categorized_projects | sort: "importance" %}
  <!-- Generate cards for each project -->
  {% if page.horizontal %}
  <div class="container">
    <div class="row row-cols-1 row-cols-md-2">
    {% for project in sorted_projects %}
      {% include projects_horizontal.liquid %}
    {% endfor %}
    </div>
  </div>
  {% else %}
  <div class="row row-cols-1 row-cols-md-3">
    {% for project in sorted_projects %}
      {% include projects.liquid %}
    {% endfor %}
  </div>
  {% endif %}
  {% endfor %}

{% else %}

<!-- Display projects without categories -->

{% assign sorted_projects = site.projects | sort: "importance" %}

  <!-- Generate cards for each project -->

{% if page.horizontal %}

  <div class="container">
    <div class="row row-cols-1 row-cols-md-2">
    {% for project in sorted_projects %}
      {% include projects_horizontal.liquid %}
    {% endfor %}
    </div>
  </div>
  {% else %}
  <div class="row row-cols-1 row-cols-md-3">
    {% for project in sorted_projects %}
      {% include projects.liquid %}
    {% endfor %}
  </div>
  {% endif %}
{% endif %}
</div>
