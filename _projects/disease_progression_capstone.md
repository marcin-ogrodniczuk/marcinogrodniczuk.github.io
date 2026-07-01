---
layout: page
title: Clinical Deterioration Prediction
description: Machine learning model for predicting progression to a critical condition from EHR-style patient trajectories.
img: assets/img/capstone_feature_comparison.png
importance: 1
category: capstone
---

This capstone project explores whether longitudinal patient data can be used to predict progression to a critical condition. The project uses daily EHR-style observations including blood pressure, heart rate, respiratory rate, temperature, oxygen saturation, medication adherence, symptom severity, and a binary progression outcome.

The workflow included exploratory data analysis, missing-value and outlier review, patient-level feature engineering, supervised classification, cross-validation, early-window testing, and a Streamlit application for model interaction.

**Problem.** Healthcare teams often need to identify patients who may deteriorate before the condition becomes critical. This project frames that task as a binary classification problem.

**Approach.** Daily records were converted into patient-level features that summarize clinical status and change over time. Logistic Regression, Random Forest, and Gradient Boosting models were compared using held-out testing and stratified cross-validation.

**Key finding.** The full 30-day and 7-day trajectory models achieved perfect internal test performance, while the 1-day baseline model performed much worse. This suggests that short-term patient trajectory information is far more informative than a single baseline observation.

**Important limitation.** The dataset appears highly separable and likely synthetic, so results should be interpreted as a complete applied machine learning workflow rather than as a clinically validated tool.

The interactive model interface is available from the [Model App]({{ '/model-app/' | relative_url }}) page.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/capstone_daily_vital_trends.png" title="Daily vital trends by outcome" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Daily clinical trajectories showed strong separation between patients who progressed and those who did not.
</div>

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/capstone_feature_comparison.png" title="Patient feature comparison" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/capstone_confusion_matrix.png" title="Best model confusion matrix" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    The project combined exploratory analysis, model comparison, and clear reporting of limitations.
</div>
