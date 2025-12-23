import numpy as np
import pandas as pd

# ------------------------------------------------------------
# 1) Cleaning & Typkonvertierung
# ------------------------------------------------------------
def clean_and_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    - Konvertiert Datentypen robust
    - Entfernt ungültige / unplausible Werte
    - Entfernt Duplikate
    """
    df = df.copy()

    # --- Robuste Typkonvertierung (object -> numeric)
    numeric_cols = ["lat", "lon", "region", "mds", "mcg", "status"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # --- Zeitstempel (Nanosekunden)
    df["time"] = pd.to_datetime(df["time"], unit="ns", errors="coerce")

    # --- Entferne Zeilen mit fehlenden essentiellen Feldern
    essential_cols = ["time", "lat", "lon", "region"]
    df = df.dropna(subset=essential_cols)

    # --- Plausibilitätschecks Geokoordinaten
    df = df[df["lat"].between(-90, 90)]
    df = df[df["lon"].between(-180, 180)]

    # --- Nicht-negative Werte (physikalisch sinnvoll)
    for col in ["mds", "mcg"]:
        if col in df.columns:
            df = df[df[col].isna() | (df[col] >= 0)]

    # --- Fehlende numerische Werte behandeln (Median)
    for col in ["mds", "mcg", "status"]:
        if col in df.columns and df[col].isna().any():
            df[col] = df[col].fillna(df[col].median())

    # --- Duplikate entfernen
    df = df.drop_duplicates(subset=["time", "lat", "lon"])

    return df


# ------------------------------------------------------------
# 2) Feature Engineering (Zeit)
# ------------------------------------------------------------
def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Erzeugt zeitbasierte Features aus dem Zeitstempel.
    """
    df = df.copy()

    df["year"] = df["time"].dt.year
    df["month"] = df["time"].dt.month
    df["day"] = df["time"].dt.day
    df["hour"] = df["time"].dt.hour
    df["minute"] = df["time"].dt.minute
    df["second"] = df["time"].dt.second

    return df