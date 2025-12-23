# src/viz.py
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

import cartopy.crs as ccrs
import cartopy.feature as cfeature


def _save_or_show(save_path: str | None) -> None:
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.tight_layout()
        plt.savefig(save_path, dpi=150)
        plt.close()
    else:
        plt.tight_layout()
        plt.show()


def plot_strikes_per_region(df, save_path: str | None = None) -> None:
    plt.figure(figsize=(8, 5))
    df["region"].value_counts().sort_index().plot(kind="bar")
    plt.title("Häufigkeit der Blitze pro Region")
    plt.ylabel("Anzahl der Blitze")
    plt.xlabel("Region")
    plt.xticks(rotation=0)
    _save_or_show(save_path)


def plot_strikes_by_hour(df, save_path: str | None = None) -> None:
    plt.figure(figsize=(10, 6))
    df.groupby("hour").size().reindex(range(24), fill_value=0).plot(kind="line", marker="o")
    plt.title("Blitzeinschläge über den Tag (Stunden)")
    plt.xlabel("Stunde des Tages")
    plt.ylabel("Anzahl der Blitze")
    plt.xticks(range(24))
    plt.grid(True)
    _save_or_show(save_path)


def plot_geo_intensity(df, save_path: str | None = None) -> None:
    plt.figure(figsize=(10, 8))
    sns.scatterplot(
        x="lon",
        y="lat",
        data=df,
        hue="mcg",
        size="mcg",
        alpha=0.3,
        palette="viridis",
        legend=False,
    )
    plt.title("Geografische Verteilung der Blitzeinschläge nach Intensität (mcg)")
    plt.xlabel("Längengrad (lon)")
    plt.ylabel("Breitengrad (lat)")
    _save_or_show(save_path)


def plot_geo_intensity_map(
    df,
    save_path: str | None = None,
    *,
    sample_n: int = 200_000,
    global_view: bool = True,
) -> None:
    """
    Geografische Darstellung der Blitze mit Basemap + Ländergrenzen.

    - CRS korrekt für lon/lat in Grad: PlateCarree()
    - Optionales Sampling für Performance
    - Optional globale Ansicht oder Auto-Zoom auf Datenbereich
    - Gridlines mit Labels für bessere Lesbarkeit
    """
    fig = plt.figure(figsize=(12, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())

    # Ansicht: global oder Auto-Zoom auf Datenbereich
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

    # Basemap Features
    ax.add_feature(cfeature.LAND, facecolor="lightgray", zorder=0)
    ax.add_feature(cfeature.OCEAN, facecolor="lightblue", zorder=0)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.8, zorder=1)
    ax.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.8, zorder=1)
    ax.add_feature(cfeature.LAKES, alpha=0.35, zorder=0)
    ax.add_feature(cfeature.RIVERS, alpha=0.25, zorder=0)

    # Gridlines (Koordinatenbeschriftung)
    gl = ax.gridlines(draw_labels=True, linewidth=0.2, alpha=0.5, linestyle="--")
    gl.top_labels = False
    gl.right_labels = False

    # Sampling (Performance)
    plot_df = df
    if sample_n is not None and len(df) > sample_n:
        plot_df = df.sample(sample_n, random_state=42)

    sc = ax.scatter(
        plot_df["lon"],
        plot_df["lat"],
        c=plot_df["mcg"],
        s=2,              # etwas kleiner für dichte Punktwolken
        cmap="viridis",
        alpha=0.25,       # etwas transparenter -> weniger "Nebel"
        transform=ccrs.PlateCarree(),  # Input-Koordinaten sind lon/lat in Grad
        zorder=2,
    )

    cbar = plt.colorbar(sc, ax=ax, shrink=0.7, pad=0.02)
    cbar.set_label("Blitzintensität (mcg)")

    title = "Geografische Verteilung der Blitze (Basemap + Ländergrenzen)"
    if sample_n is not None and len(df) > sample_n:
        title += f" (Sample: {sample_n:,})"
    ax.set_title(title)

    _save_or_show(save_path)


def plot_intensity_hist(df, save_path: str | None = None) -> None:
    plt.figure(figsize=(8, 5))
    sns.histplot(df["mcg"], bins=50, kde=True)
    plt.title("Verteilung der Blitzintensität (mcg)")
    plt.xlabel("mcg Wert")
    plt.ylabel("Häufigkeit")
    _save_or_show(save_path)


def plot_corr_heatmap(corr, save_path: str | None = None) -> None:
    plt.figure(figsize=(9, 7))
    sns.heatmap(corr, cmap="viridis")
    plt.title("Korrelationsmatrix")
    _save_or_show(save_path)


def plot_mcg_by_region(df, save_path: str | None = None) -> None:
    plt.figure(figsize=(10, 5))
    sns.boxplot(x="region", y="mcg", data=df)
    plt.title("mcg (Intensität) nach Region (Boxplot)")
    plt.xlabel("Region")
    plt.ylabel("mcg")
    _save_or_show(save_path)


def plot_mcg_by_hour(df, save_path: str | None = None) -> None:
    plt.figure(figsize=(12, 5))
    sns.boxplot(x="hour", y="mcg", data=df)
    plt.title("mcg (Intensität) nach Stunde (Boxplot)")
    plt.xlabel("Stunde")
    plt.ylabel("mcg")
    _save_or_show(save_path)