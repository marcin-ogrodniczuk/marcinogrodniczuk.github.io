---
layout: page
title: Clinical Disease Progression Model User Interface
permalink: /model-app/
description: Interactive Streamlit model interface for the clinical deterioration capstone.
nav: true
nav_order: 4
---

This application allows users to enter a simulated patient profile, specify whether a patient's recent health trajectory is stable, improving, or deteriorating, and estimate the probability that the patient will progress to a critical condition.

**Problem.** This project investigates whether patient health trajectories can be used to identify individuals at elevated risk of progressing to a critical condition before significant clinical deterioration occurs.

**Approach.** Simulated daily EHR-style data were transformed into patient-level features that summarize both current clinical status and short-term trends over time. Logistic Regression, Random Forest, and Gradient Boosting models were trained and evaluated using cross-validation, held-out test data, and early-prediction experiments across multiple observation windows.

**Result.** Models were trained using 30-day, 7-day, and 1-day observation windows. The 30-day and 7-day windows achieved perfect model performance, whereas the 1-day model performed significantly worse. These findings suggest that the dataset is likely synthetic and contains strong trajectory-based predictive signals. However, because the data are simulated, the results should be treated as a valuable demonstration of an end-to-end machine learning pipeline rather than evidence of clinical validity.

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
