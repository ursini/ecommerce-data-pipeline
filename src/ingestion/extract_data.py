from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = BASE_DIR / "data" / "raw"


def extract_customers():
    file_path = RAW_DATA_DIR / "customers.csv"

    customers = pd.read_csv(file_path)

    return customers