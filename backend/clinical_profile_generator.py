from datetime import date
from hashlib import sha256 # Simulation algorithm, because using random() will give diff val every activation ,
# based on DME,DR,risk score and age using probability


SEVERITY_RANK = {
    "Low": 1,
    "Moderate": 2,
    "High": 3,
    "Critical": 4,
}


def calculate_age(date_of_birth, today=None):
    if date_of_birth is None:
        return None

    today = today or date.today()
    birth_date = date_of_birth

    if hasattr(birth_date, "date"):
        birth_date = birth_date.date()

    return today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )


def deterministic_probability(patient_id, field_name):
    key = f"{patient_id}:{field_name}".encode("utf-8")
    value = int(sha256(key).hexdigest()[:8], 16)
    return (value % 100) / 100


def probability_flag(patient_id, field_name, probability):
    probability = max(0, min(1, probability))
    return int(deterministic_probability(patient_id, field_name) < probability)


def summarize_patient_analysis(patient_id, scan_sessions_df, analysis_results_df):
    patient_sessions = scan_sessions_df[
        scan_sessions_df["patient_id"].astype(str) == str(patient_id)
    ]

    if patient_sessions.empty:
        return {
            "max_risk_score": 0,
            "max_severity": "Low",
            "has_dme": False,
            "has_retinopathy": False,
            "has_pdr": False,
        }

    session_ids = set(patient_sessions["session_id"])
    patient_results = analysis_results_df[
        analysis_results_df["session_id"].isin(session_ids)
    ]

    if patient_results.empty:
        return {
            "max_risk_score": 0,
            "max_severity": "Low",
            "has_dme": False,
            "has_retinopathy": False,
            "has_pdr": False,
        }

    severity_values = patient_results["severity_level"].dropna()
    max_severity = "Low"
    if not severity_values.empty:
        max_severity = max(
            severity_values,
            key=lambda severity: SEVERITY_RANK.get(severity, 0)
        )

    return {
        "max_risk_score": patient_results["risk_score"].max(),
        "max_severity": max_severity,
        "has_dme": (patient_results["DME"] == 1).any(),
        "has_retinopathy": patient_results["DR"].isin(["NPDR", "PDR"]).any(),
        "has_pdr": (patient_results["DR"] == "PDR").any(),
    }


def build_medical_profile(patient_id, date_of_birth, analysis_summary):
    age = calculate_age(date_of_birth)
    risk_score = analysis_summary["max_risk_score"]
    severity = analysis_summary["max_severity"]
    has_dme = analysis_summary["has_dme"]
    has_retinopathy = analysis_summary["has_retinopathy"]
    has_pdr = analysis_summary["has_pdr"]

    high_risk = risk_score >= 80 or severity in ["High", "Critical"]
    moderate_risk = risk_score >= 50 or severity == "Moderate"
    older_than_60 = age is not None and age >= 60
    older_than_50 = age is not None and age >= 50

    diabetes_probability = 0.45
    family_history_probability = 0.25
    hypertension_probability = 0.30
    vision_probability = 0.20
    previous_eye_disease_probability = 0.15

    if moderate_risk:
        diabetes_probability += 0.25
        family_history_probability += 0.10
        hypertension_probability += 0.15
        vision_probability += 0.30
        previous_eye_disease_probability += 0.25

    if high_risk:
        diabetes_probability = 0.95
        hypertension_probability += 0.15
        vision_probability = 0.90
        previous_eye_disease_probability = 0.85

    if has_dme:
        diabetes_probability += 0.10
        vision_probability += 0.10

    if has_retinopathy:
        previous_eye_disease_probability += 0.15
        vision_probability += 0.10

    if has_pdr:
        previous_eye_disease_probability = 0.95
        vision_probability = 0.95

    if older_than_50:
        diabetes_probability += 0.10
        family_history_probability += 0.05

    if older_than_60:
        hypertension_probability += 0.25
        vision_probability += 0.10
        previous_eye_disease_probability += 0.05

    diabetes = probability_flag(patient_id, "diabetes", diabetes_probability)
    vision_problems = probability_flag(
        patient_id,
        "vision_problems",
        vision_probability
    )
    previous_eye_disease = probability_flag(
        patient_id,
        "previous_eye_disease",
        previous_eye_disease_probability
    )

    if high_risk:
        diabetes = 1
        vision_problems = 1
        previous_eye_disease = 1

    return {
        "diabetes": diabetes,
        "family_history_diabetes": probability_flag(
            patient_id,
            "family_history_diabetes",
            family_history_probability
        ),
        "hypertension": probability_flag(
            patient_id,
            "hypertension",
            hypertension_probability
        ),
        "vision_problems": vision_problems,
        "previous_eye_disease": previous_eye_disease,
    }
