# from communication.model_query import DataQueries


# def main():
#     dq = DataQueries()
#
#     # ---- CHECK GET DATA QUERIES ----
#
#     # CHECK FOR GET_PATIENT_BY_ID FUNCTION
#     # EXISTING PATIENT 1221
#
#     patient = dq.get_patient_by_id("1221")
#     print(patient)
#
#     #PATIENT 3000 DOES NOT EXIST
#
#     patient = dq.get_patient_by_id("3000")
#     if not patient.empty:
#         print(patient)
#
#     #CHECK FOR GET_PATIENT_SCAN_SESSIONS FUNCTION
#     #EXISTING PATIENT 1221
#     scan_sessions = dq.get_patient_scan_sessions("1221")
#     if not scan_sessions.empty:
#         print(scan_sessions)
#     scan_sessions = dq.get_patient_scan_sessions("12A1")
#
#     if not scan_sessions.empty:
#         print(scan_sessions)
#
#     #PATIENT WITHOUT SCAN SESSION / DOES NOT EXIST
#     scan_sessions = dq.get_patient_scan_sessions("3000")
#     if not scan_sessions.empty:
#         print(scan_sessions)
#
#     #CHECK FOR GET_PATIENT_ANALYSIS_RESULTS FUNCTION
#     analysis_results = dq.get_patient_analysis_results("1221")
#
#     if not analysis_results.empty:
#         print(analysis_results)
#
#     analysis_results = dq.get_patient_analysis_results("3000")
#
#     if not analysis_results.empty:
#         print(analysis_results)
#
#     analysis_results = dq.get_patient_analysis_results("12A1")
#
#     if not analysis_results.empty:
#         print(analysis_results)
#
#
#     #CHECK GET HIGH RISK CASES FUNCTION
#
#     high_risk_cases, count = dq.get_high_risk_cases()
#
#     if not high_risk_cases.empty:
#         print(high_risk_cases)
#         print("Total high risk cases:", count)
#
#
#     #---- CHECK INSERT DATA QUERIES ----
#
#     dq.insert_patient(
#         patient_id="4321",
#         full_name="Test",
#         date_of_birth="1999-01-01",
#         gender="Female",
#         phone=None,
#         email=None,
#         consent_status=True
#     )
#
#     patient = dq.get_patient_by_id("4321")
#
#     if not patient.empty: # PRINTS THE NEW PATIENT DATA
#         print(patient)
#
#
#     #---- CHECK INSERT ANALYSIS RESULT ----
#
#    # valid insert
#     dq.insert_analysis_result(
#         session_id=1,
#         modality="Fundus",
#         image_name="test_image.jpg",
#         DME=1,
#         DR="PDR",
#         confidence_score=0.92
#     )
#
#     # invalid session_id
#     dq.insert_analysis_result(
#         session_id="abc",
#         modality="Fundus",
#         image_name="test_image.jpg",
#         DME=1,
#         DR="PDR",
#         confidence_score=0.92
#     )
#
#
#     dq.insert_analysis_result(
#         session_id=1,
#         modality="MRI",
#         image_name="test_image.jpg",
#         DME=1,
#         DR="PDR",
#         confidence_score=0.92
#     )
#
#
#     dq.insert_analysis_result(
#         session_id=1,
#         modality="Fundus",
#         image_name="test_image.jpg",
#         DME=5,
#         DR="PDR",
#         confidence_score=0.92
#     )
#
#     # invalid confidence_score
#     dq.insert_analysis_result(
#         session_id=1,
#         modality="Fundus",
#         image_name="test_image.jpg",
#         DME=1,
#         DR="PDR",
#         confidence_score=1.5
#     )
#





#     dq.close_connection()
#
# if __name__ == "__main__":
#     main()