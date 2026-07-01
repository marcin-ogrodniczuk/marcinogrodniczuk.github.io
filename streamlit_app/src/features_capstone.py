from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

VITAL_COLUMNS = [
    'bp_systolic',
    'bp_diastolic',
    'heart_rate',
    'respiratory_rate',
    'temperature',
    'oxygen_saturation',
    'med_adherence',
    'symptom_severity',
]

REQUIRED_COLUMNS = ['patient_id', 'day', *VITAL_COLUMNS, 'progressed_to_critical']

@dataclass(frozen=True)
class RiskCategory:
    label: str
    action: str

def validate_raw_data(df: pd.DataFrame) -> None:
    """Raise an error when the source dataset does not match the project schema."""
    missing = sorted(set(REQUIRED_COLUMNS) - set(df.columns))
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")

def _slope(values: np.ndarray) -> float:
    values = np.asarray(values, dtype=float)
    if len(values) < 2:
        return 0.0
    x = np.arange(len(values), dtype=float)
    return float(np.polyfit(x, values, 1) [0])

def make_patient_features(df: pd.DataFrame) -> pd.DataFrame:
    """Convert daily EHR rows into one patient-level modeling row per patient."""
    validate_raw_data(df)
    rows: list[dict[str, float]] = []

    for patient_id, patient_df in df.groupby('patient_id', sort=False):
        patient_df = patient_df.sort_values('day')
        row: dict[str, float] = {
            'patient_id': patient_id,
            'days_observed': float(patient_df['day'].nunique()),
            'progressed_to_critical': int(patient_df['progressed_to_critical'].iloc[0]),
        }

        for col in VITAL_COLUMNS:
            values = patient_df[col].astype(float).to_numpy()
            row[f"{col}_mean"] = float(np.mean(values))
            row[f"{col}_std"] = float(np.std(values, ddof=0))
            row[f"{col}_min"] = float(np.min(values))
            row[f"{col}_max"] = float(np.max(values))
            row[f"{col}_first"] = float(values[0])
            row[f"{col}_last"] = float(values[-1])
            row[f"{col}_delta"] = float(values[-1] - values[0])
            row[f"{col}_slope"] = _slope(values)

        rows.append(row)
    return pd.DataFrame(rows)

def make_demo_sequence(
        *,
        bp_systolic: float,
        bp_diastolic: float,
        heart_rate: float,
        respiratory_rate: float,
        temperature: float,
        oxygen_saturation: float,
        med_adherence: float,
        symptom_severity: float,
        trajectory: str,
        days: int = 30,
) -> pd.DataFrame:
    """Build a synthetic 30 day patient history from app inputs."""
    end_values = {
    'bp_systolic': bp_systolic,
    'bp_diastolic': bp_diastolic,
    'heart_rate': heart_rate,
    'respiratory_rate': respiratory_rate,
    'temperature': temperature,
    'oxygen_saturation': oxygen_saturation,
    'med_adherence': med_adherence,
    'symptom_severity': symptom_severity
    }

    if trajectory == 'Deteriorating':
        start_values = {
            'bp_systolic': bp_systolic - 8 ,
            'bp_diastolic': bp_diastolic - 4,
            'heart_rate': heart_rate - 8 ,
            'respiratory_rate': respiratory_rate - 3,
            'temperature': temperature - 0.6,
            'oxygen_saturation': oxygen_saturation + 2,
            'med_adherence': min(1.0, med_adherence + 0.12),
            'symptom_severity': max(0.0, symptom_severity - 1.5),
        }
    elif trajectory == 'Improving':
        start_values = {
            'bp_systolic': bp_systolic + 8,
            'bp_diastolic': bp_diastolic + 4,
            'heart_rate': heart_rate + 8,
            'respiratory_rate': respiratory_rate + 3,
            'temperature': temperature + 0.6,
            'oxygen_saturation': oxygen_saturation - 2,
            'med_adherence': max(0.0, med_adherence - 0.12),
            'symptom_severity': symptom_severity + 1.5
        }
    else:
        start_values = end_values

    rows = []
    for day in range(1, days + 1):
        weight = (day - 1) / max(days - 1, 1)
        row = {'patient_id': 0, 'day': day, 'progressed_to_critical': 0}
        for col in VITAL_COLUMNS:
            row[col] = start_values[col] + weight * (end_values[col] - start_values[col])
        rows.append(row)
    return pd.DataFrame(rows)

def categorize_risk(probability: float) -> RiskCategory:
    if probability >= 0.65:
        return RiskCategory('High', 'Prioritize follow-up and consider clinical review.')
    if probability >= 0.35:
        return RiskCategory('Moderate', 'Monitor closely and verify recent symptoms/vitals.')
    return RiskCategory('Low', 'Continue to follow routine monitoring unless new symptoms emerge.')
