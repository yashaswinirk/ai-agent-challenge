import pandas as pd
import numpy as np

def safe_float(value):
    if pd.isna(value) or value is None or (isinstance(value, str) and value.strip() == ''):
        return np.nan
    try:
        clean_value = str(value).replace(',', '').replace('₹', '').strip()
        if clean_value in ('-', '--', ' '):
            return np.nan
        return float(clean_value)
    except ValueError:
        return np.nan

def read_csv(csv_path):
    return pd.read_csv(csv_path)
