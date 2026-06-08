import pandas as pd
import mysql.connector
from backend.db_connector import connect_to_database
from backend.table import build_analysis_result
from backend.errors import (
    handle_empty_df,
    validate_patient_input, validate_patient_id,
    validate_analysis_result_input
)



class DataQueries:
    def __init__(self, connection=None):
        self.connection = connection or connect_to_database()

        self.df_patient = pd.DataFrame()
        self.df_scan_sessions = pd.DataFrame()
        self.df_analysis_results = pd.DataFrame()
        self.df_high_risk_cases = pd.DataFrame()

    def run_query(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params or ())
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=cursor.column_names)
        cursor.close()
        return df


# GET DATA QUERIES

    def get_patient_by_id(self, patient_id):
        try:
            validate_patient_id(patient_id)
        except Exception as e:
            print(e)
            return pd.DataFrame()

        query = """
        SELECT *
        FROM Patient
        WHERE patient_id = %s
        """

        self.df_patient = self.run_query(query, (patient_id,))
        return handle_empty_df(self.df_patient, "Patient was not found")


    def get_patient_scan_sessions(self, patient_id):
        try:
            validate_patient_id(patient_id)

        except Exception as e:
            print(e)
            return pd.DataFrame()

        query = """
        SELECT *
        FROM Scan_Session
        WHERE patient_id = %s
        ORDER BY session_date DESC
        """

        self.df_scan_sessions = self.run_query(query, (patient_id,))
        return handle_empty_df(self.df_scan_sessions, "Scan session was not found")


    def get_patient_analysis_results(self, patient_id):

        try:
            validate_patient_id(patient_id)

        except Exception as e:
            print(e)
            return pd.DataFrame()

        query = """
        SELECT 
            p.patient_id,
            s.session_id,
            s.session_date,
            s.scan_type,
            a.modality,
            a.image_name,
            a.DME,
            a.DR,
            a.confidence_score,
            a.risk_score,
            a.severity_level,
            a.clinical_summary,
            a.recommendation,
            a.analysis_date
        FROM Patient p
        INNER JOIN Scan_Session s
            ON p.patient_id = s.patient_id
        INNER JOIN Analysis_Results a
            ON s.session_id = a.session_id
        WHERE p.patient_id = %s
        ORDER BY a.analysis_date DESC
        """

        self.df_analysis_results = self.run_query(query, (patient_id,))

        return handle_empty_df(
            self.df_analysis_results,
            "No analysis results were found for this patient"
        )


    def get_high_risk_cases(self):
        query = """
        SELECT 
            p.patient_id,
            s.session_id,
            a.modality,
            a.image_name,
            a.DME,
            a.DR,
            a.confidence_score,
            a.risk_score,
            a.severity_level,
            a.clinical_summary,
            a.recommendation,
            a.analysis_date
        FROM Patient p
        INNER JOIN Scan_Session s
            ON p.patient_id = s.patient_id
        INNER JOIN Analysis_Results a
            ON s.session_id = a.session_id
        WHERE a.risk_score >= 80
           OR a.severity_level IN ('High', 'Critical')
        ORDER BY a.risk_score DESC, p.date_of_birth ASC
        """

        try:
            self.df_high_risk_cases = self.run_query(query)
            count = len(self.df_high_risk_cases)

            if self.df_high_risk_cases.empty:
                print("No high risk cases were found")
            else:
                print(f"Found {count} high risk cases")

            return self.df_high_risk_cases, count

        except Exception as e:
            print(f"Database error: {e}")
            return pd.DataFrame(), 0

    def get_latest_medical_profile(self, patient_id):

        query = """
        SELECT
            mp.*,
            ss.session_date,
            ss.scan_type
        FROM Medical_Profile mp
        INNER JOIN Scan_Session ss
            ON mp.session_id = ss.session_id
        WHERE mp.patient_id = %s
        ORDER BY mp.profile_date DESC
        LIMIT 1
        """

        return self.run_query(query, (patient_id,))

    def get_medical_profile_by_session(self, session_id):
        if not isinstance(session_id, int):
            print("Session ID must be an integer")
            return pd.DataFrame()

        query = """
        SELECT
            mp.*,
            ss.session_date,
            ss.scan_type
        FROM Medical_Profile mp
        INNER JOIN Scan_Session ss
            ON mp.session_id = ss.session_id
        WHERE mp.session_id = %s
        """

        return handle_empty_df(
            self.run_query(query, (session_id,)),
            "Medical profile was not found for this session"
        )


# INSERT DATA QUERIES

    def insert_patient(self, patient_id, full_name=None, date_of_birth=None,
                       gender=None, phone=None, email=None, consent_status=True):

        try:
            validate_patient_input(
                patient_id,
                full_name,
                date_of_birth,
                gender,
                phone,
                email
            )
        except Exception as e:
            print(e)
            return

        query = """
        INSERT INTO Patient
        (patient_id, full_name, date_of_birth, gender, phone, email)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor = self.connection.cursor()

        try:
            cursor.execute(query, (
                patient_id,
                full_name,
                date_of_birth,
                gender,
                phone,
                email
            ))

            self.connection.commit()
            print("Patient inserted successfully")

        except mysql.connector.errors.IntegrityError:
            print("Patient already exists")

        except mysql.connector.errors.DatabaseError as e:
            print(f"Database error: {e}")

        finally:
            cursor.close()

    def insert_analysis_result(self, session_id, modality, image_name, DME, DR,
                               confidence_score=None):

        try:
            validate_analysis_result_input(
                session_id,
                modality,
                image_name,
                DME,
                DR,
                confidence_score
            )

        except Exception as e:
            print(e)
            return

        query = """
        INSERT INTO Analysis_Results
        (
            session_id,
            modality,
            image_name,
            DME,
            DR,
            confidence_score,
            risk_score,
            severity_level,
            clinical_summary,
            recommendation,
            analysis_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURDATE())
        """

        cursor = self.connection.cursor()
        result = build_analysis_result(
            session_id=session_id,
            modality=modality,
            image_name=image_name,
            dme=DME,
            dr=DR,
            confidence_score=confidence_score
        )

        try:
            cursor.execute(query, (
                result["session_id"],
                result["modality"],
                result["image_name"],
                result["DME"],
                result["DR"],
                result["confidence_score"],
                result["risk_score"],
                result["severity_level"],
                result["clinical_summary"],
                result["recommendation"]
            ))

            self.connection.commit()
            print("Analysis result inserted successfully")

        except mysql.connector.errors.IntegrityError as e:
            print(f"Integrity error: {e}")

        except mysql.connector.errors.DatabaseError as e:
            print(f"Database error: {e}")

        finally:
            cursor.close()




    def close_connection(self):
        self.connection.close()
