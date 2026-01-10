# src/analysis.py
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def print_basic_overview(df: pd.DataFrame) -> None:
    """
    Print basic structural information and a preview of the dataset.
    """
    print(df.info())
    print("\nData successfully loaded.")
    print(f"Dataset contains {df.shape[1]} columns and {df.shape[0]} rows")

    print("\nMissing values per column:")
    print(df.isnull().sum())

    print("\nFirst five rows of the dataset:")
    print(df.head())


def print_uniques(df: pd.DataFrame) -> None:
    """
    Print unique values for selected categorical or temporal columns if present.
    """
    if "region" in df.columns:
        print("\nUnique values in column 'region':")
        print(df["region"].unique())

    if "year" in df.columns:
        print("\nUnique values in column 'year':")
        print(df["year"].unique())

    if "month" in df.columns:
        print("\nUnique values in column 'month':")
        print(df["month"].unique())


def print_time_range(df: pd.DataFrame) -> None:
    """
    Print the minimum and maximum timestamps in the dataset.
    """
    if "time" not in df.columns:
        return

    tmin = df["time"].min()
    tmax = df["time"].max()

    print("\nTime range in dataset:")
    print(f"Min: {tmin} | Max: {tmax}")


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute a correlation matrix for relevant numeric features.
    """
    cols = [
        "lat", "lon", "region", "mds", "mcg", "status",
        "year", "month", "day", "hour", "minute", "second",
    ]
    cols = [c for c in cols if c in df.columns]
    return df[cols].corr(numeric_only=True)


def top_correlations(corr: pd.DataFrame, target: str, n: int = 5) -> pd.Series:
    """
    Return the top n features with the strongest absolute correlation
    to the target variable.
    """
    if target not in corr.columns:
        return pd.Series(dtype=float)

    s = corr[target].drop(labels=[target]).dropna()
    s = s.reindex(s.abs().sort_values(ascending=False).index)
    return s.head(n)


def linear_regression_mcg(
    df: pd.DataFrame,
    feature_cols: list[str] | None = None,
    target_col: str = "mcg",
    test_size: float = 0.2,
    random_state: int = 42,
) -> dict:
    """
    Fit a simple linear regression model to predict the target variable
    and return evaluation metrics and coefficients.
    """
    if feature_cols is None:
        candidate = ["mds", "hour", "region", "lat", "lon", "month"]
        feature_cols = [c for c in candidate if c in df.columns]

    needed = feature_cols + [target_col]
    d = df[needed].dropna().copy()

    if len(d) < 10:
        return {
            "ok": False,
            "reason": f"Not enough data after dropna(): {len(d)} rows",
            "features": feature_cols,
            "target": target_col,
        }

    X = d[feature_cols]
    y = d[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    coef = pd.Series(
        model.coef_, index=feature_cols
    ).sort_values(key=np.abs, ascending=False)

    return {
        "ok": True,
        "model": model,
        "features": feature_cols,
        "target": target_col,
        "n_rows": len(d),
        "test_size": test_size,
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2),
        "intercept": float(model.intercept_),
        "coefficients": coef,
    }


def print_regression_report(result: dict) -> None:
    """
    Print a concise console report of the regression results.
    """
    if not result.get("ok", False):
        print("\n--- LINEAR REGRESSION ---")
        print("Not executed:", result.get("reason", "unknown"))
        return

    print("\n--- LINEAR REGRESSION ---")
    print(f"Target: {result['target']}")
    print(f"Features: {result['features']}")
    print(f"N (after dropna): {result['n_rows']}, Test size: {result['test_size']}")

    print(f"MAE:  {result['mae']:.3f}")
    print(f"RMSE: {result['rmse']:.3f}")
    print(f"R²:   {result['r2']:.3f}")

    print("\nCoefficients (sorted by |coef|):")
    print(result["coefficients"])
    print(f"\nIntercept: {result['intercept']:.3f}")