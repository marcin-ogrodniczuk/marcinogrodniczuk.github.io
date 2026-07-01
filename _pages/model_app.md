---
layout: page
title: Model App
permalink: /model-app/
description: Interactive Streamlit model interface for the clinical deterioration capstone.
nav: true
nav_order: 4
---

This page is the deployed model location for the capstone project. The interface lets a user enter a simulated patient profile, choose whether the
recent trajectory is stable, improving, or deteriorating, and receive an estimated probability of progression to a critical condition.

**Problem.** The project asks whether patient trajectories can be used to identify higher-risk patients before deterioration becomes critical.

**Approach.** Daily EHR-style observations were converted into patient-level features that summarize current values and short-term change over time.
Logistic Regression, Random Forest, and Gradient Boosting models were compared using held-out testing, cross-validation, and early-window experiments.

**Result.** The 30-day, 7-day, 3-day, and 2-day trajectory models produced perfect internal performance, while the 1-day model performed much worse.
This suggests that the synthetic dataset contains strong trajectory-based signals, but the results should be interpreted as a demonstration of an
end-to-end machine learning workflow rather than a clinically validated tool.

{% assign app_url = site.streamlit_app_url | default: "" %}
{% if app_url != "" %}
<p>
  <a href="{{ app_url }}" target="_blank" rel="noopener noreferrer">Open app full screen</a>
</p>

<iframe
  src="{{ app_url }}?embed=true"
  title="Clinical Deterioration Risk Dashboard"
  style="width: 100%; height: 900px; border: 1px solid var(--global-divider-color); border-radius: 6px;"
  loading="lazy"
></iframe>
{% else %}
<div style="border: 1px solid var(--global-divider-color); border-radius: 6px; padding: 1rem; margin: 1rem 0;">
  The Streamlit app files are included in this repository under <code>streamlit_app/</code>. After the app is deployed on Streamlit Community Cloud,
  add the deployed URL to <code>streamlit_app_url</code> in <code>_config.yml</code> and this page will embed the live interface here.
</div>

**Deployment target.**

- Repository: `marcin-ogrodniczuk/marcinogrodniczuk.github.io`
- Branch: `main`
- Main file path: `streamlit_app/app_capstone.py`
{% endif %}

<div style="display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));">
    <div>
        {% include figure.liquid loading="eager" path="assets/img/capstone_feature_comparison.png" %}
    </div>
    <div>
        {% include figure.liquid loading="eager" path="assets/img/capstone_confusion_matrix.png" %}
    </div>
</div>
<div class="caption">
    The app is designed to make the model workflow visible to non-technical users through plain-language outputs and interactive controls.
</div>
