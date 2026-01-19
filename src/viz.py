import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

import cartopy.crs as ccrs
import cartopy.feature as cfeature


def _save_or_show(save_path: str | None) -> None:
    """
    Speichert die aktuell aktive Matplotlib-Figur oder zeigt sie an.

    Falls ``save_path`` gesetzt ist, wird die Grafik als Datei gespeichert.
    Andernfalls wird die Grafik interaktiv angezeigt.

    Parameter
    ---------
    save_path:
        Zielpfad für die Ausgabe-Datei oder ``None`` zum Anzeigen der Grafik.

    Rückgabewert
    ------------
    None
    """
    plt.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=150)
        plt.close()
    else:
        plt.show()


def plot_strikes_per_region(df, save_path: str | None = None) -> None:
    """
    Visualisiert die Anzahl der detektierten Blitze pro Region.

    Erstellt ein Balkendiagramm der Ereignishäufigkeit je ``region``-ID.

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
    plt.xlabel("Region")
    plt.ylabel("Count")
    plt.xticks(rotation=0)
    _save_or_show(save_path)


def plot_strikes_by_hour(df, save_path: str | None = None) -> None:
    """
    Visualisiert die Anzahl der detektierten Blitze nach Tagesstunde.

    Erstellt ein Liniendiagramm der Ereignishäufigkeit je Stunde (0–23).
    Fehlende Stunden werden mit 0 aufgefüllt.

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
    (
        df.groupby("hour")
        .size()
        .reindex(range(24), fill_value=0)
        .plot(kind="line", marker="o")
    )
    plt.title("Lightning strikes by hour of day")
    plt.xlabel("Hour")
    plt.ylabel("Count")
    plt.xticks(range(24))
    plt.grid(True)
    _save_or_show(save_path)


def plot_geo_map(
    df,
    save_path: str | None = None,
    *,
    sample_n: int = 200_000,
    global_view: bool = True,
) -> None:
    """
    Visualisiert Blitzeinschläge auf einer Karte (Punktdaten + Kartenelemente).

    Die Ereignisse werden als Punkte in geografischen Koordinaten dargestellt.
    Die Farbskala kodiert den Wert der Spalte ``mcg``.

    Parameter
    ---------
    df:
        Bereinigter DataFrame mit ``lat``, ``lon`` und ``mcg``.
    save_path:
        Optionaler Speicherpfad für die Grafik.
    sample_n:
        Maximale Anzahl zufällig gezogener Datenpunkte zur Performance-Optimierung.
        Wenn ``df`` größer ist als ``sample_n``, wird eine Stichprobe gezogen.
    global_view:
        Falls True, wird eine globale Kartenansicht verwendet. Andernfalls wird
        automatisch auf den Datenbereich gezoomt.

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
    cbar.set_label("mcg")

    title = "Geographic distribution of lightning strikes"
    if sample_n is not None and len(df) > sample_n:
        title += f" (sample: {sample_n:,})"
    ax.set_title(title)

    _save_or_show(save_path)


def plot_mcg_hist(df, save_path: str | None = None) -> None:
    """
    Visualisiert die Verteilung von ``mcg`` als Histogramm.

    Ergänzend wird eine Dichtekurve (KDE) angezeigt, um die Verteilung
    glatter interpretieren zu können.

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
    plt.title("Distribution of mcg")
    plt.xlabel("mcg")
    plt.ylabel("Frequency")
    _save_or_show(save_path)


def plot_corr_heatmap(corr, save_path: str | None = None) -> None:
    """
    Visualisiert eine Korrelationsmatrix als Heatmap.

    Parameter
    ---------
    corr:
        Korrelationsmatrix als DataFrame (z. B. Ergebnis von ``df.corr()``).
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
    Visualisiert die Verteilung von ``mcg`` nach Region mittels Boxplots.

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
    plt.title("mcg by region")
    plt.xlabel("Region")
    plt.ylabel("mcg")
    _save_or_show(save_path)