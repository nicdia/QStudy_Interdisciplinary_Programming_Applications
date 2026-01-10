import numpy as np
import pandas as pd


def clean_and_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the dataset by converting data types, removing invalid values,
    handling missing data, and dropping duplicates.
    """
    df = df.copy()

    numeric_cols = ["lat", "lon", "region", "mds", "mcg", "status"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["time"] = pd.to_datetime(df["time"], unit="ns", errors="coerce")

    essential_cols = ["time", "lat", "lon", "region"]
    df = df.dropna(subset=essential_cols)

    df = df[df["lat"].between(-90, 90)]
    df = df[df["lon"].between(-180, 180)]

    for col in ["mds", "mcg"]:
        if col in df.columns:
            df = df[df[col].isna() | (df[col] >= 0)]

    for col in ["mds", "mcg", "status"]:
        if col in df.columns and df[col].isna().any():
            df[col] = df[col].fillna(df[col].median())

    df = df.drop_duplicates(subset=["time", "lat", "lon"])

    return df


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create additional time-based features from a datetime column.
    """
    df = df.copy()

    df["year"] = df["time"].dt.year
    df["month"] = df["time"].dt.month
    df["day"] = df["time"].dt.day
    df["hour"] = df["time"].dt.hour
    df["minute"] = df["time"].dt.minute
    df["second"] = df["time"].dt.second

    return df