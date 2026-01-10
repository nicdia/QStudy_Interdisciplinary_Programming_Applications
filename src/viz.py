import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

import cartopy.crs as ccrs
import cartopy.feature as cfeature


def _save_or_show(save_path: str | None) -> None:
    """
    Speichert die aktuell aktive Matplotlib-Figur oder zeigt sie an.

    Falls ein Speicherpfad angegeben ist, wird:
    - das Zielverzeichnis (inkl. Elternverzeichnisse) erstellt,
    - das Layout optimiert,
    - die Figur als PNG-Datei gespeichert,
    - und anschließend geschlossen.

    Falls kein Speicherpfad angegeben ist, wird die Figur direkt angezeigt.

    Parameter
    ---------
    save_path:
        Zielpfad für die Ausgabe-Datei oder ``None`` zum Anzeigen der Grafik.

    Rückgabewert
    ------------
    None
    """
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.tight_layout()
        plt.savefig(save_path, dpi=150)
        plt.close()
    else:
        plt.tight_layout()
        plt.show()


def plot_strikes_per_region(df, save_path: str | None = None) -> None:
    """
    Visualisiert die Anzahl der Blitzeinschläge pro Region.

    Erstellt ein Balkendiagramm auf Basis der Häufigkeit der ``region``-IDs.
    Die Darstellung beantwortet die Frage, in welchen Regionen besonders viele
    Blitze detektiert wurden.

    Parameter
    ---------
    df:
        Bereinigter DataFrame mit einer ``region``-Spalte.
    save_path:
        Optionaler Speicherpfad für die Grafik.

    Rückgabewert
    ------------
    None
    """
    plt.figure(figsize=(8, 5))
    df["region"].value_counts().sort_index().plot(kind="bar")
    plt.title("Lightning strikes per region")
    plt.ylabel("Count")
    plt.xlabel("Region")
    plt.xticks(rotation=0)
    _save_or_show(save_path)


def plot_strikes_by_hour(df, save_path: str | None = None) -> None:
    """
    Visualisiert die Anzahl der Blitzeinschläge nach Tagesstunde.

    Das Liniendiagramm zeigt die zeitliche Verteilung der Ereignisse über
    24 Stunden und beantwortet die Frage, zu welchen Tageszeiten Blitze
    besonders häufig auftreten.

    Parameter
    ---------
    df:
        Bereinigter DataFrame mit einer ``hour``-Spalte.
    save_path:
        Optionaler Speicherpfad für die Grafik.

    Rückgabewert
    ------------
    None
    """
    plt.figure(figsize=(10, 6))
    df.groupby("hour").size().reindex(range(24), fill_value=0).plot(
        kind="line", marker="o"
    )
    plt.title("Lightning strikes by hour of day")
    plt.xlabel("Hour")
    plt.ylabel("Count")
    plt.xticks(range(24))
    plt.grid(True)
    _save_or_show(save_path)


def plot_geo_intensity(
    df,
    save_path: str | None = None,
    *,
    sample_n: int = 200_000,
) -> None:
    """
    Visualisiert die geografische Verteilung der Blitzintensität als Streudiagramm.

    Jeder Punkt entspricht einem Blitzeinschlag, eingefärbt nach ``mcg``
    (Blitzintensität). Für sehr große Datensätze wird optional eine Stichprobe
    gezogen, um die Performance zu verbessern.

    Parameter
    ---------
    df:
        Bereinigter DataFrame mit ``lat``, ``lon`` und ``mcg``.
    save_path:
        Optionaler Speicherpfad für die Grafik.
    sample_n:
        Maximale Anzahl zufällig gezogener Datenpunkte (Standard: 200.000).

    Rückgabewert
    ------------
    None
    """
    plot_df = df
    if sample_n is not None and len(df) > sample_n:
        plot_df = df.sample(sample_n, random_state=42)

    plt.figure(figsize=(10, 8))
    sc = plt.scatter(
        plot_df["lon"],
        plot_df["lat"],
        c=plot_df["mcg"],
        s=2,
        alpha=0.25,
    )
    plt.title("Geographic distribution of lightning intensity (mcg)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    cbar = plt.colorbar(sc, shrink=0.8)
    cbar.set_label("Lightning intensity (mcg)")
    _save_or_show(save_path)


def plot_geo_intensity_map(
    df,
    save_path: str | None = None,
    *,
    sample_n: int = 200_000,
    global_view: bool = True,
) -> None:
    """
    Visualisiert Blitzeinschläge auf einer geografischen Karte mit Basemap.

    Die Funktion kombiniert Punktdaten mit kartografischen Elementen
    (Land, Ozeane, Grenzen) und stellt die Blitzintensität farbcodiert dar.
    Optional kann eine globale Ansicht oder ein automatischer Zoom auf
    den Datenbereich gewählt werden.

    Parameter
    ---------
    df:
        Bereinigter DataFrame mit ``lat``, ``lon`` und ``mcg``.
    save_path:
        Optionaler Speicherpfad für die Grafik.
    sample_n:
        Maximale Anzahl zufällig gezogener Datenpunkte zur Performance-Optimierung.
    global_view:
        Falls True, wird eine globale Kartenansicht verwendet.

    Rückgabewert
    ------------
    None
    """
    fig = plt.figure(figsize=(12, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())

    if global_view:
        ax.set_global()
    else:
        min_lon, max_lon = df["lon"].min(), df["lon"].max()
        min_lat, max_lat = df["lat"].min(), df["lat"].max()
        pad_lon = max(1.0, (max_lon - min_lon) * 0.05)
        pad_lat = max(1.0, (max_lat - min_lat) * 0.05)
        ax.set_extent(
            [min_lon - pad_lon, max_lon + pad_lon, min_lat - pad_lat, max_lat + pad_lat],
            crs=ccrs.PlateCarree(),
        )

    ax.add_feature(cfeature.LAND, facecolor="lightgray", zorder=0)
    ax.add_feature(cfeature.OCEAN, facecolor="lightblue", zorder=0)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.8, zorder=1)
    ax.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.8, zorder=1)
    ax.add_feature(cfeature.LAKES, alpha=0.35, zorder=0)
    ax.add_feature(cfeature.RIVERS, alpha=0.25, zorder=0)

    gl = ax.gridlines(draw_labels=True, linewidth=0.2, alpha=0.5, linestyle="--")
    gl.top_labels = False
    gl.right_labels = False

    plot_df = df
    if sample_n is not None and len(df) > sample_n:
        plot_df = df.sample(sample_n, random_state=42)

    sc = ax.scatter(
        plot_df["lon"],
        plot_df["lat"],
        c=plot_df["mcg"],
        s=2,
        alpha=0.25,
        transform=ccrs.PlateCarree(),
        zorder=2,
    )

    cbar = plt.colorbar(sc, ax=ax, shrink=0.7, pad=0.02)
    cbar.set_label("Lightning intensity (mcg)")

    title = "Geographic distribution of lightning strikes"
    if sample_n is not None and len(df) > sample_n:
        title += f" (sample: {sample_n:,})"
    ax.set_title(title)

    _save_or_show(save_path)


def plot_intensity_hist(df, save_path: str | None = None) -> None:
    """
    Visualisiert die Verteilung der Blitzintensität als Histogramm.

    Das Histogramm (inkl. optionaler Dichtekurve) zeigt, wie häufig
    bestimmte ``mcg``-Werte auftreten und gibt Aufschluss über
    Schiefe und Streuung der Intensitätsverteilung.

    Parameter
    ---------
    df:
        Bereinigter DataFrame mit einer ``mcg``-Spalte.
    save_path:
        Optionaler Speicherpfad für die Grafik.

    Rückgabewert
    ------------
    None
    """
    plt.figure(figsize=(8, 5))
    sns.histplot(df["mcg"], bins=50, kde=True)
    plt.title("Distribution of lightning intensity (mcg)")
    plt.xlabel("mcg")
    plt.ylabel("Frequency")
    _save_or_show(save_path)


def plot_corr_heatmap(corr, save_path: str | None = None) -> None:
    """
    Visualisiert eine Korrelationsmatrix als Heatmap.

    Die Farbskala ermöglicht eine schnelle Identifikation
    starker positiver oder negativer Zusammenhänge zwischen Variablen.

    Parameter
    ---------
    corr:
        Korrelationsmatrix als DataFrame.
    save_path:
        Optionaler Speicherpfad für die Grafik.

    Rückgabewert
    ------------
    None
    """
    plt.figure(figsize=(9, 7))
    sns.heatmap(corr, cmap="viridis")
    plt.title("Correlation matrix")
    _save_or_show(save_path)


def plot_mcg_by_region(df, save_path: str | None = None) -> None:
    """
    Visualisiert die Blitzintensität nach Region mittels Boxplots.

    Die Darstellung erlaubt einen Vergleich der Verteilung von ``mcg``
    zwischen Regionen und macht Unterschiede in Median, Streuung
    und Ausreißern sichtbar.

    Parameter
    ---------
    df:
        Bereinigter DataFrame mit ``region`` und ``mcg``.
    save_path:
        Optionaler Speicherpfad für die Grafik.

    Rückgabewert
    ------------
    None
    """
    plt.figure(figsize=(10, 5))
    sns.boxplot(x="region", y="mcg", data=df)
    plt.title("Lightning intensity (mcg) by region")
    plt.xlabel("Region")
    plt.ylabel("mcg")
    _save_or_show(save_path)


def plot_mcg_by_hour(df, save_path: str | None = None) -> None:
    """
    Visualisiert die Blitzintensität nach Tagesstunde mittels Boxplots.

    Diese Darstellung beantwortet die Frage, ob sich Intensität und
    Streuung der Blitze im Tagesverlauf systematisch verändern.

    Parameter
    ---------
    df:
        Bereinigter DataFrame mit ``hour`` und ``mcg``.
    save_path:
        Optionaler Speicherpfad für die Grafik.

    Rückgabewert
    ------------
    None
    """
    plt.figure(figsize=(12, 5))
    sns.boxplot(x="hour", y="mcg", data=df)
    plt.title("Lightning intensity (mcg) by hour")
    plt.xlabel("Hour")
    plt.ylabel("mcg")
    _save_or_show(save_path)