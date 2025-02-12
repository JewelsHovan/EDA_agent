import pandas as pd

def load_csv(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

def load_parquet(file_path: str) -> pd.DataFrame:
    return pd.read_parquet(file_path)

