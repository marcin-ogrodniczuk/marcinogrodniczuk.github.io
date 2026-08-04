---
layout: about
title: Home
permalink: /
subtitle: Healthcare Data Scientist | Applied AI | LLM Engineering

profile:
  align: right
  image: prof_pic.jpg
  image_circular: false # crops the image to make it circular
  more_info: >
    <p>Healthcare AI agents</p>
    <p>Clinical data science</p>
    <p>Python, SQL, LangGraph</p>

selected_papers: false # includes a list of papers marked as "selected={true}"
social: true # includes social icons at the bottom of the page

announcements:
  enabled: false # includes a list of news items
  scrollable: true # adds a vertical scroll bar if there are more than 3 news items
  limit: 5 # leave blank to include all the news in the `_news` folder

latest_posts:
  enabled: false
  scrollable: true # adds a vertical scroll bar if there are more than 3 new posts items
  limit: 3 # leave blank to include all the blog posts
---

<link rel="stylesheet" href="{{ '/assets/css/marcin.css' | relative_url }}">

<div class="marcin-home">
  <section class="home-hero">
    <p class="eyebrow">Healthcare Data Science + Applied AI</p>
    <p class="hero-copy">
      I am a data scientist with a biomedical research background, focused on healthcare analytics, machine learning, and production-minded AI systems. I like projects where messy clinical or operational data becomes something useful: a model, dashboard, agent workflow, or decision-support tool that people can inspect and trust.
    </p>
    <div class="hero-actions">
      <a class="site-button primary" href="{{ '/projects/' | relative_url }}">View Projects</a>
      <a class="site-button" href="https://github.com/marcin-ogrodniczuk">GitHub</a>
    </div>
  </section>

  <section>
    <div class="focus-grid">
      <article class="focus-tile">
        <span>01</span>
        <h3>Healthcare AI Agents</h3>
        <p>LangGraph, LangChain RAG, structured outputs, guardrails, tool calling, and evaluation harnesses for operations workflows.</p>
      </article>
      <article class="focus-tile">
        <span>02</span>
        <h3>Clinical Machine Learning</h3>
        <p>Patient-level feature engineering, model comparison, validation, and honest reporting of limitations in EHR-style datasets.</p>
      </article>
      <article class="focus-tile">
        <span>03</span>
        <h3>Analytics Products</h3>
        <p>Python, SQL, dashboards, and user-facing applications that make data easier to reason about and act on.</p>
      </article>
    </div>
  </section>

  <section>
    <div class="section-heading">
      <h2>Featured Work</h2>
      <a href="{{ '/projects/' | relative_url }}">All projects</a>
    </div>
    <div class="project-list">
      <a class="project-row" href="{{ '/projects/healthcare_operations_copilot/' | relative_url }}">
        <span class="project-meta">LLM Engineering</span>
        <h3>Healthcare Operations Copilot</h3>
        <p>A production-style agent MVP for referral intake, payer policy retrieval, operational tool calling, guardrails, human review flags, and LLMOps-style evaluation.</p>
      </a>
      <a class="project-row" href="{{ '/projects/disease_progression_capstone/' | relative_url }}">
        <span class="project-meta">Machine Learning</span>
        <h3>Clinical Deterioration Prediction</h3>
        <p>A supervised learning workflow using longitudinal EHR-style patient trajectories, feature engineering, cross-validation, and a Streamlit model interface.</p>
      </a>
      <a class="project-row" href="{{ '/projects/rag_biomedical_literature/' | relative_url }}">
        <span class="project-meta">Retrieval-Augmented Generation</span>
        <h3>Biomedical Literature RAG Pipeline</h3>
        <p>A local RAG system for querying PubMed-style biomedical literature with source-grounded retrieval and citation-aware answers.</p>
      </a>
    </div>
  </section>

  <section>
    <div class="section-heading">
      <h2>Core Skills</h2>
    </div>
    <div class="skill-strip">
      <span>Python</span>
      <span>SQL</span>
      <span>Machine Learning</span>
      <span>Healthcare Analytics</span>
      <span>FastAPI</span>
      <span>LangGraph</span>
      <span>LangChain</span>
      <span>RAG</span>
      <span>LLMOps</span>
      <span>Docker</span>
    </div>
  </section>
</div>
