import pandas as pd


def clean_and_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the dataset by converting types, removing invalid values, imputing missing
    values with sensible defaults, and dropping duplicates.
    """
    df = df.copy()

    numeric_cols = ["lat", "lon", "region", "mds", "mcg", "status"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "time" in df.columns:
        df["time"] = pd.to_datetime(df["time"], unit="ns", errors="coerce")

    essential_cols = [c for c in ["time", "lat", "lon", "region"] if c in df.columns]
    df = df.dropna(subset=essential_cols)

    if "lat" in df.columns:
        df = df[df["lat"].between(-90, 90)]
    if "lon" in df.columns:
        df = df[df["lon"].between(-180, 180)]

    for col in ["mds", "mcg"]:
        if col in df.columns:
            df = df[df[col].isna() | (df[col] >= 0)]

    # Impute signal-like columns with median
    for col in ["mds", "mcg"]:
        if col in df.columns and df[col].isna().any():
            df[col] = df[col].fillna(df[col].median())

    # Impute code-like columns with mode (more sensible than median)
    for col in ["status", "region"]:
        if col in df.columns and df[col].isna().any():
            mode_val = df[col].mode(dropna=True)
            fill_val = mode_val.iloc[0] if len(mode_val) else 0
            df[col] = df[col].fillna(fill_val)

    # Cast region/status to more appropriate types (memory + semantics)
    if "region" in df.columns:
        df["region"] = df["region"].round().astype("Int64")
    if "status" in df.columns:
        df["status"] = df["status"].round().astype("Int64")

    # Deduplicate (include region to avoid merging same coords/time across regions)
    subset = [c for c in ["time", "lat", "lon", "region"] if c in df.columns]
    if subset:
        df = df.drop_duplicates(subset=subset)

    return df


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create additional time-based features from a datetime column.
    """
    df = df.copy()
    if "time" not in df.columns:
        return df

    df["year"] = df["time"].dt.year
    df["month"] = df["time"].dt.month
    df["day"] = df["time"].dt.day
    df["hour"] = df["time"].dt.hour
    df["minute"] = df["time"].dt.minute
    df["second"] = df["time"].dt.second

    return df