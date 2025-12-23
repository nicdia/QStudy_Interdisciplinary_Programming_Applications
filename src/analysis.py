# src/analysis.py
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ------------------------------------------------------------
# 1) Reporting / Überblick
# ------------------------------------------------------------
def print_basic_overview(df: pd.DataFrame) -> None:
    print(df.info())
    print("\nDaten erfolgreich geladen.")
    print(f"Der Datensatz enthält {df.shape[1]} Spalten und {df.shape[0]} Zeilen")

    print("\nAnzahl der fehlenden Werte pro Spalte:")
    print(df.isnull().sum())

    print("\nDie ersten fünf Zeilen des Datensatzes:")
    print(df.head())


def print_uniques(df: pd.DataFrame) -> None:
    if "region" in df.columns:
        print("\nDie eindeutigen Werte in der Region 'region' sind:")
        print(df["region"].unique())

    if "year" in df.columns:
        print("\nDie eindeutigen Werte in der Spalte 'year' sind:")
        print(df["year"].unique())

    if "month" in df.columns:
        print("\nDie eindeutigen Werte in der Spalte 'month' sind:")
        print(df["month"].unique())


def print_time_range(df: pd.DataFrame) -> None:
    """Hilft, Aussagen wie 'nur Nov/Dez 2025' datenbasiert zu begründen."""
    if "time" not in df.columns:
        return
    tmin = df["time"].min()
    tmax = df["time"].max()
    print("\nZeitraum im Datensatz:")
    print(f"Min: {tmin} | Max: {tmax}")


# ------------------------------------------------------------
# 2) Korrelation
# ------------------------------------------------------------
def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    cols = ["lat", "lon", "region", "mds", "mcg", "status", "year", "month", "day", "hour", "minute", "second"]
    cols = [c for c in cols if c in df.columns]
    return df[cols].corr(numeric_only=True)


def top_correlations(corr: pd.DataFrame, target: str, n: int = 5) -> pd.Series:
    """
    Gibt die stärksten linearen Zusammenhänge (nach Betrag) zur Zielvariable aus.
    """
    if target not in corr.columns:
        return pd.Series(dtype=float)

    s = corr[target].drop(labels=[target]).dropna()
    s = s.reindex(s.abs().sort_values(ascending=False).index)
    return s.head(n)


# ------------------------------------------------------------
# 3) Regression (scikit-learn) – minimal & bewertungsfest
# ------------------------------------------------------------
def linear_regression_mcg(
    df: pd.DataFrame,
    feature_cols: list[str] | None = None,
    target_col: str = "mcg",
    test_size: float = 0.2,
    random_state: int = 42,
) -> dict:
    """
    Einfache lineare Regression: mcg aus wenigen Features vorhersagen.
    - Minimal, aber zeigt ML/Regression
    - Gibt Metriken + Koeffizienten zurück
    """

    if feature_cols is None:
        # bewusst simpel: Ort/Zeit/Signal
        candidate = ["mds", "hour", "region", "lat", "lon", "month"]
        feature_cols = [c for c in candidate if c in df.columns]

    needed = feature_cols + [target_col]
    d = df[needed].dropna().copy()

    # Falls zu wenige Daten vorhanden sind: sauber abbrechen
    if len(d) < 10:
        return {
            "ok": False,
            "reason": f"Zu wenige Daten für Regression nach dropna(): {len(d)} Zeilen",
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

    coef = pd.Series(model.coef_, index=feature_cols).sort_values(key=np.abs, ascending=False)

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
    Konsolen-Output für euer main.py (damit ihr eine schöne Auswertung habt).
    """
    if not result.get("ok", False):
        print("\n--- REGRESSION (Linear) ---")
        print("Nicht ausgeführt:", result.get("reason", "unbekannt"))
        return

    print("\n--- REGRESSION (Linear) ---")
    print(f"Target: {result['target']}")
    print(f"Features: {result['features']}")
    print(f"N (nach dropna): {result['n_rows']}, Testsize: {result['test_size']}")

    print(f"MAE:  {result['mae']:.3f}")
    print(f"RMSE: {result['rmse']:.3f}")
    print(f"R²:   {result['r2']:.3f}")

    print("\nKoeffizienten (nach Einfluss |coef| sortiert):")
    print(result["coefficients"])
    print(f"\nIntercept: {result['intercept']:.3f}")