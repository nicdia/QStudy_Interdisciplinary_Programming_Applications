import pandas as pd
from pathlib import Path

USECOLS = ["time", "lat", "lon", "region", "mds", "mcg", "status"]

def load_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path, usecols=USECOLS)

def ensure_output_dirs(base_dir: str = "../output") -> None:
    Path(base_dir).mkdir(parents=True, exist_ok=True)
    Path(f"{base_dir}/figures").mkdir(parents=True, exist_ok=True)

def export_clean_data(df: pd.DataFrame, out_path: str) -> None:
    df.to_csv(out_path, index=False)
    print(f"\nBereinigte Daten exportiert nach: {out_path}")