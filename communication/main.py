from backend.csv_loader import load_csv
from backend.db_connector import connect_to_database, execute_sql_file
from backend.table import (
    patient,
    medical_profile,
    scan_session,
    fundus,
    oct,
    analysis_results,
    insert_table_to_sql
)
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
CSV_DIR = BASE_DIR / "backend" / "csv_files"
DATABASE_SCHEMA = BASE_DIR / "backend" / "database" / "tables.sql"


def main():

    # CSV LOAD
    fundus_df = load_csv(CSV_DIR / "EYE FUNDUS.csv")
    oct_df = load_csv(CSV_DIR / "OCT.csv")

    print("\nCSV files loaded successfully")

    # DB CONNECTION
    execute_sql_file(DATABASE_SCHEMA)
    connection = connect_to_database()

    # TABLES
    patient_table = patient(fundus_df, oct_df)
    scan_session_table = scan_session(fundus_df, oct_df)
    fundus_table = fundus(fundus_df, scan_session_table)
    oct_table = oct(oct_df, scan_session_table)
    analysis_table = analysis_results(fundus_df, oct_df, scan_session_table)
    medical_profile_table = medical_profile(
        scan_session_table,
        patient_table,
        analysis_table
    )



    tables = [
        patient_table,
        scan_session_table,
        medical_profile_table,
        fundus_table,
        oct_table,
        analysis_table
    ]

    for table in tables:
        insert_table_to_sql(connection, table)





    connection.close()


if __name__ == "__main__":
    main()
