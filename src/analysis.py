import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def print_basic_overview(df: pd.DataFrame, *, head_n: int = 5) -> None:
    """
    Gibt einen kompakten Überblick über den Datensatz aus.

    Diese Hilfsfunktion dient als schneller Plausibilitäts-Check und gibt aus:
    - Struktur und Datentypen des DataFrames (über ``df.info()``)
    - Anzahl der Zeilen und Spalten
    - Anzahl fehlender Werte pro Spalte
    - Eine Vorschau der ersten Zeilen

    Parameter
    ---------
    df:
        Zu untersuchender DataFrame.
    head_n:
        Anzahl der Zeilen, die in der Vorschau angezeigt werden (Standard: 5).

    Rückgabewert
    ------------
    None
        Die Funktion gibt ausschließlich Informationen auf der Konsole aus.
    """
    print(df.info())
    print("\nData successfully loaded.")
    print(f"Dataset contains {df.shape[1]} columns and {df.shape[0]} rows")

    print("\nMissing values per column:")
    print(df.isnull().sum())

    print(f"\nFirst {head_n} rows of the dataset:")
    print(df.head(head_n))


def print_uniques(df: pd.DataFrame) -> None:
    """
    Gibt eindeutige Werte ausgewählter Spalten aus.

    Diese Funktion wird genutzt, um:
    - die Abdeckung kategorialer Variablen (z. B. Regionen)
    - sowie den zeitlichen Umfang (Jahre, Monate)
    nach der Feature-Erzeugung schnell zu überprüfen.

    Parameter
    ---------
    df:
        Eingabe-DataFrame.

    Rückgabewert
    ------------
    None
        Die Funktion gibt ausschließlich Informationen auf der Konsole aus.
    """
    if "region" in df.columns:
        print("\nUnique values in column 'region':")
        print(pd.Series(df["region"].dropna().unique()).sort_values().to_list())

    if "year" in df.columns:
        print("\nUnique values in column 'year':")
        print(pd.Series(df["year"].dropna().unique()).sort_values().to_list())

    if "month" in df.columns:
        print("\nUnique values in column 'month':")
        print(pd.Series(df["month"].dropna().unique()).sort_values().to_list())


def print_time_range(df: pd.DataFrame) -> None:
    """
    Gibt den minimalen und maximalen Zeitstempel im Datensatz aus.

    Parameter
    ---------
    df:
        Eingabe-DataFrame mit einer ``time``-Spalte vom Typ ``datetime``.

    Rückgabewert
    ------------
    None

    Hinweise
    --------
    Falls keine ``time``-Spalte vorhanden ist, wird nichts ausgegeben.
    """
    if "time" not in df.columns:
        return

    tmin = df["time"].min()
    tmax = df["time"].max()

    print("\nTime range in dataset:")
    print(f"Min: {tmin} | Max: {tmax}")


def print_time_granularity(df: pd.DataFrame) -> None:
    """
    Gibt einfache Kennzahlen zur zeitlichen Abdeckung des Datensatzes aus.

    Die Funktion ermittelt:
    - Anzahl unterschiedlicher Tage
    - Anzahl unterschiedlicher Monate

    Diese Kennzahlen unterstützen Aussagen über den zeitlichen Umfang
    des Datensatzes (z. B. „12 Tage über 2 Monate“).

    Parameter
    ---------
    df:
        Eingabe-DataFrame mit einer ``time``-Spalte vom Typ ``datetime``.

    Rückgabewert
    ------------
    None

    Hinweise
    --------
    Falls die ``time``-Spalte fehlt oder leer ist, erfolgt keine Ausgabe.
    """
    if "time" not in df.columns:
        return

    s = df["time"].dropna()
    if s.empty:
        return

    unique_days = s.dt.date.nunique()
    unique_months = (s.dt.year.astype(str) + "-" + s.dt.month.astype(str).str.zfill(2)).nunique()

    print("\nTime coverage stats:")
    print(f"Unique days: {unique_days}")
    print(f"Unique months: {unique_months}")


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Berechnet eine Pearson-Korrelationsmatrix für ausgewählte numerische Variablen.

    Die Analyse beschränkt sich bewusst auf fachlich sinnvolle Merkmale
    (räumlich, zeitlich und signalbezogen), um die Interpretierbarkeit
    der Korrelationsmatrix zu gewährleisten.

    Parameter
    ---------
    df:
        Bereinigter und um Zeitfeatures erweiterter DataFrame.

    Rückgabewert
    ------------
    pandas.DataFrame
        Quadratische Korrelationsmatrix mit Werten zwischen -1 und 1.
        Spalten, die im DataFrame nicht vorhanden sind, werden ignoriert.
    """
    cols = [
        "lat", "lon", "region", "mds", "mcg",
        "month", "day", "hour", "minute", "second",
    ]
    cols = [c for c in cols if c in df.columns]
    return df[cols].corr(numeric_only=True)


def top_correlations(corr: pd.DataFrame, target: str, n: int = 5) -> pd.Series:
    """
    Ermittelt die stärksten linearen Zusammenhänge mit einer Zielvariable.

    Aus einer Korrelationsmatrix wird:
    - die Zielspalte extrahiert,
    - die Selbstkorrelation entfernt,
    - nach dem Betrag der Korrelation sortiert (Vorzeichen bleibt erhalten),
    - und die Top-n-Korrelationen zurückgegeben.

    Parameter
    ---------
    corr:
        Korrelationsmatrix (z. B. aus :func:`correlation_matrix`).
    target:
        Name der Zielvariable (muss in ``corr`` enthalten sein).
    n:
        Anzahl der stärksten Korrelationen (Standard: 5).

    Rückgabewert
    ------------
    pandas.Series
        Rangliste der Variablen mit stärkstem linearem Zusammenhang zur Zielvariable.

    Hinweise
    --------
    Ist die Zielvariable nicht enthalten, wird eine leere Series zurückgegeben.
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
    *,
    one_hot_region: bool = True,
) -> dict:
    """
    Trainiert und evaluiert ein lineares Regressionsmodell zur Vorhersage der Blitzintensität.

    Es wird ein einfaches ``LinearRegression``-Modell (scikit-learn) verwendet,
    um die Zielvariable (Standard: ``mcg``) aus ausgewählten Einflussgrößen
    vorherzusagen. Das Modell dient primär der explorativen Analyse.

    Die Regionsvariable kann optional als kategoriales Merkmal per One-Hot-Encoding
    behandelt werden (empfohlen), da Regions-IDs keine ordinalen Werte darstellen.

    Parameter
    ---------
    df:
        Bereinigter und feature-angereicherter DataFrame.
    feature_cols:
        Liste der zu verwendenden Feature-Spalten. Falls ``None``, wird
        ein projektspezifischer Standardsatz genutzt.
    target_col:
        Zielvariable der Regression (Standard: ``"mcg"``).
    test_size:
        Anteil der Daten für den Testdatensatz (Standard: 0.2).
    random_state:
        Zufalls-Seed für reproduzierbare Ergebnisse (Standard: 42).
    one_hot_region:
        Falls True, wird ``region`` als kategoriale Variable one-hot-enkodiert.

    Rückgabewert
    ------------
    dict
        Enthält u. a.:
        - Erfolgsstatus
        - Modellparameter
        - Evaluationsmetriken (MAE, RMSE, R²)
        - Regressionskoeffizienten

    Hinweise
    --------
    - Zeilen mit fehlenden Werten in Features oder Zielvariable werden entfernt.
    - Bei zu wenigen verbleibenden Datenpunkten wird kein Modell trainiert.
    - Das Modell ist bewusst einfach gehalten und nicht für produktive Vorhersagen gedacht.
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

    X = d[feature_cols].copy()
    y = d[target_col]

    if one_hot_region and "region" in X.columns:
        X["region"] = X["region"].astype("category")
        X = pd.get_dummies(X, columns=["region"], drop_first=True)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    coef = pd.Series(model.coef_, index=X.columns).sort_values(key=np.abs, ascending=False)

    return {
        "ok": True,
        "model": model,
        "features": list(X.columns),
        "target": target_col,
        "n_rows": len(d),
        "test_size": test_size,
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2),
        "intercept": float(model.intercept_),
        "coefficients": coef,
        "one_hot_region": one_hot_region,
    }


def print_regression_report(result: dict) -> None:
    """
    Gibt einen kompakten Bericht zu den Regressionsergebnissen aus.

    Parameter
    ---------
    result:
        Ergebnis-Dictionary aus :func:`linear_regression_mcg`.

    Rückgabewert
    ------------
    None

    Hinweise
    --------
    Falls ``result["ok"]`` False ist, wird lediglich der Abbruchgrund ausgegeben.
    """
    if not result.get("ok", False):
        print("\n--- LINEAR REGRESSION ---")
        print("Not executed:", result.get("reason", "unknown"))
        return

    print("\n--- LINEAR REGRESSION ---")
    print(f"Target: {result['target']}")
    print(f"Features: {result['features']}")
    print(f"One-hot region: {result.get('one_hot_region', False)}")
    print(f"N (after dropna): {result['n_rows']}, Test size: {result['test_size']}")

    print(f"MAE:  {result['mae']:.3f}")
    print(f"RMSE: {result['rmse']:.3f}")
    print(f"R²:   {result['r2']:.3f}")

    print("\nCoefficients (sorted by |coef|):")
    print(result["coefficients"])
    print(f"\nIntercept: {result['intercept']:.3f}")