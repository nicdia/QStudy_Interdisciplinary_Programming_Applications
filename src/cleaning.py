import pandas as pd


def clean_and_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Bereinigt und standardisiert den Blitzeinschlags-Datensatz.

    Die Funktion führt eine konservative, analysefreundliche Datenbereinigung durch:
    - Konvertiert ausgewählte Spalten robust in numerische Datentypen
      (ungültige Werte werden zu NaN)
    - Wandelt die Spalte ``time`` von Unix-Zeitstempeln (Nanosekunden) in
      ``datetime64[ns]`` um
    - Entfernt Einträge mit fehlenden essenziellen Informationen
      (Zeitstempel oder räumliche Zuordnung)
    - Führt Plausibilitätsprüfungen für geografische Koordinaten und Signalwerte durch
    - Ersetzt fehlende Werte mit sinnvollen Standardwerten
      (Median für Messgrößen, Modus für Codes)
    - Setzt Code-artige Spalten (z. B. ``region``, ``status``) auf einen
      semantisch passenden Integer-Datentyp
    - Entfernt Duplikate basierend auf Zeit und Ort (inkl. Region)

    Parameter
    ---------
    df:
        Rohes Eingabe-DataFrame.

    Rückgabewert
    ------------
    pandas.DataFrame
        Eine bereinigte Kopie des Eingabe-DataFrames, geeignet für
        weiterführende Analysen und Visualisierungen.

    Hinweise
    --------
    - Die Typkonvertierung verwendet ``errors="coerce"``, um fehlerhafte Werte
      nicht zum Abbruch zu bringen.
    - Der Median wird für kontinuierliche Messgrößen (``mds``, ``mcg``) genutzt,
      da er robuster gegenüber Ausreißern ist.
    - Der Modus wird für kategoriale bzw. Code-Spalten (``region``, ``status``)
      verwendet, um ungültige Zwischenwerte zu vermeiden.
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

    for col in ["mds", "mcg"]:
        if col in df.columns and df[col].isna().any():
            df[col] = df[col].fillna(df[col].median())

    for col in ["status", "region"]:
        if col in df.columns and df[col].isna().any():
            mode_val = df[col].mode(dropna=True)
            fill_val = mode_val.iloc[0] if len(mode_val) else 0
            df[col] = df[col].fillna(fill_val)

    if "region" in df.columns:
        df["region"] = df["region"].round().astype("Int64")
    if "status" in df.columns:
        df["status"] = df["status"].round().astype("Int64")

    subset = [c for c in ["time", "lat", "lon", "region"] if c in df.columns]
    if subset:
        df = df.drop_duplicates(subset=subset)

    return df


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Erzeugt zeitbasierte Zusatzfeatures aus einer ``time``-Spalte.

    Der Zeitstempel wird in einzelne Kalender- und Zeiteinheiten zerlegt:
    ``year``, ``month``, ``day``, ``hour``, ``minute`` und ``second``.
    Diese Features ermöglichen zeitliche Aggregationen (z. B. Blitze pro Stunde)
    sowie einfache statistische Auswertungen.

    Parameter
    ---------
    df:
        Eingabe-DataFrame mit einer ``time``-Spalte vom Typ ``datetime``.

    Rückgabewert
    ------------
    pandas.DataFrame
        Eine Kopie des DataFrames mit zusätzlich erzeugten Zeit-Features.

    Hinweise
    --------
    Falls keine ``time``-Spalte vorhanden ist, wird das DataFrame unverändert
    zurückgegeben.
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