import pandas as pd
from datetime import datetime
from backend.random_data import (
    random_full_name,
    random_gender,
    random_date_of_birth,
    random_phone,
    random_email,
)
from backend.clinical_profile_generator import (
    build_medical_profile,
    summarize_patient_analysis,
)



# CLASS TABLE
class Table:
    def __init__(self, table_name, data, pks=None, fks=None, ref_tables=None, refs=None):
        self.table_name = table_name
        self.data = data.where(pd.notnull(data), None)
        self.headers = self.data.columns.values

        self.pks = pks or []
        self.fks = fks or []
        self.ref_tables = ref_tables or []
        self.refs = refs or []

# HELP FUNCTIONS FOR STR MANIPULATIONS, BECAUSE THE COL NAME CONTAINS:

def extract_patient_id(image_name):
    return str(image_name)[:4]

def extract_eye_side(image_name):
    parts = str(image_name).split("_")
    if len(parts) < 2:
        return None

    eye_code = parts[1]

    if eye_code == "OD":
        return "Right"
    elif eye_code == "OI":
        return "Left"
    else:
        return None

# MAKING SURE "--" VALUE WILL REPRESENT UNKNOWN SAME AS DATABASE
def clean_dr(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value in ["-", "--", "", "nan", "None"]:
        return None

    return value


def calculate_clinical_insight(dme, dr):
    dme = int(dme) if not pd.isna(dme) else 0
    dr = clean_dr(dr)

    if dme == 1 and dr == "PDR":
        return {
            "risk_score": 95,
            "severity_level": "Critical",
            "clinical_summary": "DME is present with proliferative diabetic retinopathy.",
            "recommendation": "Urgent ophthalmology review is recommended."
        }

    if dme == 1 and dr == "NPDR":
        return {
            "risk_score": 85,
            "severity_level": "High",
            "clinical_summary": "DME is present with non-proliferative diabetic retinopathy.",
            "recommendation": "Prompt follow-up and treatment planning are recommended."
        }

    if dme == 1:
        return {
            "risk_score": 65,
            "severity_level": "Moderate",
            "clinical_summary": "DME is present without documented diabetic retinopathy.",
            "recommendation": "Follow-up evaluation is recommended."
        }

    if dr == "PDR":
        return {
            "risk_score": 80,
            "severity_level": "High",
            "clinical_summary": "Proliferative diabetic retinopathy is documented without DME.",
            "recommendation": "Urgent retinal specialist review is recommended."
        }

    if dr == "NPDR":
        return {
            "risk_score": 50,
            "severity_level": "Moderate",
            "clinical_summary": "Non-proliferative diabetic retinopathy is documented without DME.",
            "recommendation": "Routine follow-up and disease monitoring are recommended."
        }

    if dr is None:
        return {
            "risk_score": 35,
            "severity_level": "Moderate",
            "clinical_summary": "DME is not documented and DR classification is unknown.",
            "recommendation": "Review image quality and repeat classification if needed."
        }

    return {
        "risk_score": 15,
        "severity_level": "Low",
        "clinical_summary": "No DME or diabetic retinopathy is documented.",
        "recommendation": "Routine monitoring is recommended."
    }


def build_analysis_result(session_id, modality, image_name, dme, dr,
                          confidence_score=None, analysis_date=None):
    insight = calculate_clinical_insight(dme, dr)

    return {
        "session_id": session_id,
        "modality": modality,
        "image_name": image_name,
        "DME": dme,
        "DR": clean_dr(dr),
        "confidence_score": confidence_score,
        "risk_score": insight["risk_score"],
        "severity_level": insight["severity_level"],
        "clinical_summary": insight["clinical_summary"],
        "recommendation": insight["recommendation"],
        "analysis_date": analysis_date or datetime.today().date()
    }

# CREATING THE TABLES

def patient(fundus_df, oct_df):
    all_names = pd.concat([fundus_df["Name"], oct_df["Name"]], ignore_index=True)
    patient_ids = all_names.apply(extract_patient_id).drop_duplicates()

    patients = []

    for patient_id in patient_ids:
        full_name = random_full_name()

        patients.append({
            "patient_id": patient_id,
            "full_name": full_name,
            "date_of_birth": random_date_of_birth(),
            "gender": random_gender(),
            "phone": random_phone(),
            "email": random_email(full_name)
        })

    patient_df = pd.DataFrame(patients)

    return Table(
        table_name="Patient",
        data=patient_df,
        pks=["patient_id"]
    )


def scan_session(fundus_df, oct_df):
    session_date = datetime.today().date()

    fundus_patient_ids = set(fundus_df["Name"].apply(extract_patient_id))
    oct_patient_ids = set(oct_df["Name"].apply(extract_patient_id))

    all_patient_ids = sorted(fundus_patient_ids.union(oct_patient_ids))

    sessions = []
    session_id = 1

    for patient_id in all_patient_ids:
        has_fundus = patient_id in fundus_patient_ids
        has_oct = patient_id in oct_patient_ids

        if has_fundus and has_oct:
            scan_type = "Fundus, OCT"
        elif has_fundus:
            scan_type = "Fundus"
        else:
            scan_type = "OCT"

        sessions.append({
            "session_id": session_id,
            "patient_id": patient_id,
            "session_date": session_date,
            "scan_type": scan_type
        })

        session_id += 1

    scan_df = pd.DataFrame(sessions)

    return Table(
        table_name="Scan_Session",
        data=scan_df,
        pks=["session_id"],
        fks=["patient_id"],
        ref_tables=["Patient"],
        refs=["patient_id"]
    )


def medical_profile(scan_session_table, patient_table, analysis_table):
    patient_rows = patient_table.data.set_index("patient_id")
    profiles = []

    for _, session in scan_session_table.data.iterrows():
        patient_id = session["patient_id"]
        patient = patient_rows.loc[patient_id]
        analysis_summary = summarize_patient_analysis(
            patient_id,
            scan_session_table.data,
            analysis_table.data
        )
        profile = build_medical_profile(
            patient_id,
            patient["date_of_birth"],
            analysis_summary
        )

        profiles.append({
            "patient_id": patient_id,
            "diabetes": profile["diabetes"],
            "family_history_diabetes": profile["family_history_diabetes"],
            "hypertension": profile["hypertension"],
            "vision_problems": profile["vision_problems"],
            "previous_eye_disease": profile["previous_eye_disease"],
            "profile_date": datetime.today().date(),
            "session_id": session["session_id"]
        })

    medical_df = pd.DataFrame(profiles)

    return Table(
        table_name="Medical_Profile",
        data=medical_df,
        pks=["profile_id"],
        fks=["patient_id", "session_id"],
        ref_tables=["Patient", "Scan_Session"],
        refs=["patient_id", "session_id"]
    )


def fundus(fundus_df, scan_session_table):

    session_map = dict(zip(
        scan_session_table.data["patient_id"],
        scan_session_table.data["session_id"]
    ))
    #print("Fundus DR unique values:")
    #print(fundus_df["DR"].unique())

    fundus_data = pd.DataFrame({
        "session_id": fundus_df["Name"].apply(
            lambda name: session_map[extract_patient_id(name)]
        ),
        "name": fundus_df["Name"].values,
        "eye_side": fundus_df["Name"].apply(extract_eye_side),
        "DME": fundus_df["DME"].values,
        "DR": fundus_df["DR"].apply(clean_dr).values
    })

    return Table(
        table_name="Fundus",
        data=fundus_data,
        pks=["name"],
        fks=["session_id"],
        ref_tables=["Scan_Session"],
        refs=["session_id"]
    )


def oct(oct_df, scan_session_table):

    session_map = dict(zip(
        scan_session_table.data["patient_id"],
        scan_session_table.data["session_id"]
    ))

    #print("OCT DR unique values:")
    #print(oct_df["DR"].unique())

    oct_data = pd.DataFrame({
        "session_id": oct_df["Name"].apply(
            lambda name: session_map[extract_patient_id(name)]
        ),
        "name": oct_df["Name"].values,
        "eye_side": oct_df["Name"].apply(extract_eye_side),
        "DME": oct_df["DME"].values,
        "DR": oct_df["DR"].apply(clean_dr).values
    })

    return Table(
        table_name="OCT",
        data=oct_data,
        pks=["name"],
        fks=["session_id"],
        ref_tables=["Scan_Session"],
        refs=["session_id"]
    )

def analysis_results(fundus_df, oct_df, scan_session_table):
    results = []

    session_map = dict(zip(
        scan_session_table.data["patient_id"],
        scan_session_table.data["session_id"]
    ))

    for _, row in fundus_df.reset_index(drop=True).iterrows():
        patient_id = extract_patient_id(row["Name"])

        results.append(build_analysis_result(
            session_id=session_map[patient_id],
            modality="Fundus",
            image_name=row["Name"],
            dme=row["DME"],
            dr=row["DR"]
        ))

    for _, row in oct_df.reset_index(drop=True).iterrows():
        patient_id = extract_patient_id(row["Name"])

        results.append(build_analysis_result(
            session_id=session_map[patient_id],
            modality="OCT",
            image_name=row["Name"],
            dme=row["DME"],
            dr=row["DR"]
        ))

    analysis_df = pd.DataFrame(results)

    return Table(
        table_name="Analysis_Results",
        data=analysis_df,
        pks=["result_id"],
        fks=["session_id"],
        ref_tables=["Scan_Session"],
        refs=["session_id"]
    )





# INSERT TO SQL

def insert_table_to_sql(connection, table):
    cursor = connection.cursor()

    columns = list(table.data.columns)
    columns_str = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))

    sql = f"""
    INSERT INTO {table.table_name} ({columns_str})
    VALUES ({placeholders})
    """

    for _, row in table.data.iterrows():
        values = tuple(row[col] for col in columns)
        cursor.execute(sql, values)

    connection.commit()
    cursor.close()

    print(f"{table.table_name} inserted successfully")
