import pandas as pd


EXPECTED_COLUMNS = ["Name", "DME", "DR", "Size", "Format"]


def load_csv(file_path):
    df = pd.read_csv(file_path)

    validate_columns(df)
    df = clean_csv_data(df)

    return df


def validate_columns(df):
    missing_columns = []

    for col in EXPECTED_COLUMNS:
        if col not in df.columns:
            missing_columns.append(col)

    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")


def clean_csv_data(df):
    df = df.copy()
    df["Name"] = df["Name"].astype(str)
    df["Size"] = df["Size"].astype(str)
    df["Format"] = df["Format"].astype(str)
    df["DME"] = pd.to_numeric(df["DME"], errors="coerce").fillna(0).astype(int)
    df["DR"] = df["DR"].astype(str).str.strip()

    return df


def show_csv_info(df):
    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])
    print("Column names:", df.columns.tolist())

    print("\nFirst rows:")
    print(df.head())