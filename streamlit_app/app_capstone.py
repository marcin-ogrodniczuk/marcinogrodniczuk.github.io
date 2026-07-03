from __future__ import annotations

import json 
from pathlib import Path

import joblib 
import pandas as pd 
import streamlit as st 

from src.features_capstone import categorize_risk, make_demo_sequence, make_patient_features

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / 'data' / 'ehr_disease_progression.csv'
MODEL_PATH = BASE_DIR / 'models' / 'critical_progression_model.joblib'
FEATURE_PATH = BASE_DIR / 'models' / 'feature_columns.json'
METRICS_PATH = BASE_DIR / 'reports' / 'metrics.json'
EDA_FIGURES_DIR = BASE_DIR / 'reports' / 'eda'
FIGURES_DIR = BASE_DIR / 'reports' / 'figures'
MODEL_COMPARISON_PATH = BASE_DIR / 'reports' / 'model_comparison.csv'
TOP_FEATURES_PATH = BASE_DIR / 'reports' / 'top_features.csv'
EARLY_1_DAY_PATH = BASE_DIR / 'reports' / 'early_window_1_day_holdout_results.csv'
EARLY_7_DAY_PATH = BASE_DIR / 'reports' / 'early_window_7_day_holdout_results.csv'


st.set_page_config(
    page_title='Clinical Deterioration Risk Dashboard',
    page_icon='health',
    layout='wide',
)

@st.cache_data
def load_raw_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)

@st.cache_data
def load_patient_features() -> pd.DataFrame:
    return make_patient_features(load_raw_data())

@st.cache_resource
def load_model():
    if not MODEL_PATH.exists() or not FEATURE_PATH.exists():
        return None, []
    model = joblib.load(MODEL_PATH)
    feature_columns = json.loads(FEATURE_PATH.read_text(encoding='utf-8'))
    return model, feature_columns 

@st.cache_data
def load_metrics() -> dict:
    if not METRICS_PATH.exists():
        return {}
    return json.loads(METRICS_PATH.read_text(encoding='utf-8'))

def page_header(title: str, caption: str) -> None:
    st.title(title)
    st.caption(caption)

def home_page() -> None:
    page_header(
        'Clinical Deterioration Risk Dashboard', 
        'A capstone project using sequential EHR observations to predict progression to critical illness',
    )

    st.write(
        'This project translates longitudinal vital-sign and patient-behavior data into a patient-level'
         ' risk score. The workflow includes data exploration, feature engineering across 30-day patient'
         ' trajectories, supervised classification, model evaluation, and an interactive Streamlit interface.'
    )

    raw_df = load_raw_data()
    patient_df = load_patient_features()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Daily observations', f"{raw_df.shape[0]:,}")
    col2.metric('Patients', f"{patient_df.shape[0]:,}")
    col3.metric("Days per patient", f"{int(patient_df['days_observed'].median())}")
    col4.metric("Critical progression", f"{patient_df['progressed_to_critical'].mean():.1%}")

    st.subheader('Project Objective')
    st.write(
        "The objective is to help healthcare stakeholders identify patients whose recent trajectories "
        "suggest elevated risk of clinical deterioration, supporting earlier intervention and more informed "
        "resource allocation."
    )
    
def show_eda_figure(filename: str, caption: str) -> None:
    figure_path = EDA_FIGURES_DIR / filename

    if figure_path.exists():
        st.image(str(figure_path), caption=caption, use_container_width=True)
    else:
        st.warning(f'Missing EDA figure {figure_path}')

def show_report_figure(filename: str, caption: str) -> None:
    figure_path = FIGURES_DIR / filename 

    if figure_path.exists():
        st.image(str(figure_path), caption=caption, use_container_width=True)
    else:
        st.warning(f'Missing report figure: {figure_path}')


def dashboard_page() -> None:
    page_header(
        'Exploratory Dashboard', 
        "Dataset-level patterns used to understand clinical deterioration risk.", 
    )

    raw_df = load_raw_data()
    patient_df = load_patient_features()
    target_counts = patient_df['progressed_to_critical'].value_counts().rename(
        index={0: 'Not critical', 1: 'Progressed'}
    )
    col1, col2 = st.columns([1,2])
    with col1:
        st.subheader('Target Balance')
        st.bar_chart(target_counts)
    with col2:
        st.subheader('Average Patient Trajectories')
        metric = st.selectbox(
            'Clinical measure',
        [
            'bp_systolic', 
            'bp_diastolic', 
            'heart_rate',
            'respiratory_rate', 
            'temperature', 
            'oxygen_saturation', 
            'med_adherence', 
            'symptom_severity',
        ],
        )
        chart_df = (
            raw_df.groupby(['day', 'progressed_to_critical'], as_index=False)[metric]
            .mean()
            .pivot(index='day', columns='progressed_to_critical', values=metric)
            .rename(columns={0: 'Not critical', 1: 'Progressed'})
        )
        st.line_chart(chart_df)

    st.divider()
    st.subheader('EDA Visualizations')

    trend_tab, corr_tab, comparison_tab = st.tabs(
        [
            'Daily Trends', 
            'Correlation Matrix',
            'Group Comparison', 
        ]
    )

    with trend_tab:
        show_eda_figure(
            'daily_vital_trends_by_outcome.png',
            'Daily vital-sign and patient-behavior trends grouped by progression outcome.',
        )
    
    with corr_tab:
        show_eda_figure(
            'correlation_matrix.png',
            'Correlation matrix showing relationships among engineered patient-level features.'
        )

    with comparison_tab:
        show_eda_figure(
            'patient_group_feature_comparison.png',
            'Comparison of patient-level features between progressed and non-progressed groups.'
        )

    st.subheader('Patient-Level Feature Summary')
    st.dataframe(
        patient_df.drop(columns=['patient_id']).describe().T.round(3), 
        use_container_width=True,
    )


def predictor_page() -> None:
    page_header(
        "Patient Risk Predictor", 
        "Enter a current patient profile and recent trajectory pattern to estimate critical progression risk.",
    )

    model, feature_columns = load_model()
    if model is None:
        st.warning('Model artifacts are not available yet. Run `python train_model_capstone.py` first')
        return

    col1, col2, col3 = st.columns(3)
    with col1:
        bp_systolic = st.slider('Systolic blood pressure', 85.0, 190.0, 128.0, 1.0)
        bp_diastolic = st.slider('Diastolic blood pressure', 45.0, 115.0, 82.0, 1.0)
        heart_rate = st.slider('Heart rate', 45.0, 145.0, 82.0, 1.0)
    with col2: 
        respiratory_rate = st.slider('Respiratory rate', 10.0, 35.0, 19.0, 0.5)
        temperature = st.slider('Temperature', 95.0, 104.5, 98.8, 0.1)
        oxygen_saturation = st.slider('Oxygen saturation', 82.0, 100.0, 96.0, 0.5)
    with col3:
        med_adherence = st.slider('Medication adherence', 0.0, 1.0, 0.72, 0.01)
        symptom_severity = st.slider('Symptom severity', 0.0, 10.0, 4.0, 0.1)
        trajectory = st.selectbox('Recent trajectory', ['Stable', 'Deteriorating', 'Improving'])

    sequence_df = make_demo_sequence(
        bp_systolic=bp_systolic,
        bp_diastolic=bp_diastolic,
        heart_rate=heart_rate,
        respiratory_rate=respiratory_rate,
        temperature=temperature, 
        oxygen_saturation=oxygen_saturation,
        med_adherence=med_adherence,
        symptom_severity=symptom_severity,
        trajectory=trajectory,
    )
    features = make_patient_features(sequence_df).reindex(columns=['patient_id', 'progressed_to_critical', *feature_columns])
    X_pred = features[feature_columns]
    probability = float(model.predict_proba(X_pred)[0, 1])
    risk = categorize_risk(probability)

    st.subheader('Prediction')
    c1, c2, c3 = st.columns(3)
    c1.metric('Risk probability', f"{probability:.1%}")
    c2.metric('Risk category', risk.label)
    c3.metric('Trajectory', trajectory)
    st.info(risk.action)

    st.subheader('Constructed 30-day Patient History')
    st.line_chart(sequence_df.set_index('day')[['heart_rate', 'respiratory_rate', 'oxygen_saturation', 'symptom_severity']])

def model_results_page() -> None:
    page_header(
        'Model Results',
        'Model performance, interpretation, and early prediction experiments.', 
    )

    metrics = load_metrics()
    if not metrics:
        st.warning('Metrics are not available yet. run `python train_model_capstone.py` first.')
        return
    
    st.subheader('Best Model Summary')
    best_model = metrics['best_model']
    best_metrics = metrics['metrics'][best_model]

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric('Best model', best_model)
    c2.metric('Accuracy', f"{best_metrics['accuracy']:.2f}")
    c3.metric('Precision', f"{best_metrics['precision']:.2f}")
    c4.metric('Recall', f"{best_metrics['recall']:.2f}")
    c5.metric('ROC-AUC', f"{best_metrics['roc_auc']:.2f}")

    st.subheader('Model Comparison')
    if MODEL_COMPARISON_PATH.exists():
        comparison = pd.read_csv(MODEL_COMPARISON_PATH)

        if 'Unnamed: 0' in comparison.columns and 'model' not in comparison.columns:
            comparison = comparison.rename(columns={'Unnamed: 0': 'model'})
    else:
        comparison = pd.DataFrame(metrics['metrics']).T.drop(columns=['confusion_matrix']).reset_index()
        comparison = comparison.rename(columns={'index': 'model'})

    st.dataframe(comparison.round(4), use_container_width=True)

    st.subheader('ROC Curve and Confusion Matrix')
    fig_col1, fig_col2 = st.columns(2)

    with fig_col1:
        show_report_figure(
            'roc_curve.png',
            'ROC curve for the selected model. A curve near the top-left indicates strong class separation.', 
        )
    
    with fig_col2:
        show_report_figure(
            'confusion_matrix.png',
            'Confusion matrix showing correct and incorrect predictions on the held-out test set.',
        )

    st.subheader('Top Predictive Features')
    if TOP_FEATURES_PATH.exists():
        top_features = pd.read_csv(TOP_FEATURES_PATH)
    else: 
        top_features = pd.DataFrame(metrics['top_features'])
    
    st.dataframe(top_features, use_container_width=True)

    if {'feature', 'importance'}.issubset(top_features.columns):
        chart_df = top_features.head(12).set_index('feature')['importance']
        st.bar_chart(chart_df)

    st.subheader('Early Prediction Window Comparison')

    early_rows = []
    if EARLY_1_DAY_PATH.exists():
        one_day = pd.read_csv(EARLY_1_DAY_PATH)
        one_day['window'] = '1 day'
        early_rows.append(one_day)

    if EARLY_7_DAY_PATH.exists():
        seven_day = pd.read_csv(EARLY_7_DAY_PATH)
        seven_day['window'] = '7 days'
        early_rows.append(seven_day)

    if MODEL_COMPARISON_PATH.exists():
        thirty_day = pd.read_csv(MODEL_COMPARISON_PATH)

        if 'Unnamed: 0' in thirty_day.columns and 'model' not in thirty_day.columns:
            thirty_day = thirty_day.rename(columns={'Unnamed: 0': 'model'})

        thirty_day['window'] = '30 days'
        early_rows.append(thirty_day)

    if early_rows:
        early_df = pd.concat(early_rows, ignore_index=True)
        st.dataframe(early_df.round(4), use_container_width=True)

        metric_cols = [col for col in ['accuracy', 'precision', 'recall', 'f1', 'roc_auc'] if col in early_df.columns]
        if metric_cols and 'model' in early_df.columns:
            chart_df = early_df.set_index(['window', 'model'])[metric_cols]
            st.bar_chart(chart_df)
    else:
        st.info('Early-window results files are not available.')
    
    st.subheader('Important Limitation of Dataset')
    st.info(
        'The 7-day and 30-day models achieved perfect internal performance, while the 1-day model performed much worse. '
        'This suggests that the synthetic dataset contains strong trajectory-based signals. These results demonstrate the '
        'machine learning workflow, but they should not be interpreted as clinical validation.'
    )

PAGES = {
    "Home": home_page,
    'Exploratory Dashboard': dashboard_page,
    'Patient Risk Predictor': predictor_page,
    'Model Results': model_results_page,
}

selection = st.sidebar.radio('Navigation', list(PAGES.keys()))
PAGES[selection]()