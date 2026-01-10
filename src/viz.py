import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

import cartopy.crs as ccrs
import cartopy.feature as cfeature


def _save_or_show(save_path: str | None) -> None:
    """
    Save the current matplotlib figure to disk or display it.
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
    Plot the number of lightning strikes per region.
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
    Plot the number of lightning strikes by hour of day.
    """
    plt.figure(figsize=(10, 6))
    df.groupby("hour").size().reindex(range(24), fill_value=0).plot(kind="line", marker="o")
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
    Plot geographic distribution of lightning strikes colored by intensity (sampled for performance).
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
    Plot lightning strikes on a geographic map with intensity coloring (sampled for performance).
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
    Plot a histogram of lightning intensity values.
    """
    plt.figure(figsize=(8, 5))
    sns.histplot(df["mcg"], bins=50, kde=True)
    plt.title("Distribution of lightning intensity (mcg)")
    plt.xlabel("mcg")
    plt.ylabel("Frequency")
    _save_or_show(save_path)


def plot_corr_heatmap(corr, save_path: str | None = None) -> None:
    """
    Plot a heatmap of the correlation matrix.
    """
    plt.figure(figsize=(9, 7))
    sns.heatmap(corr, cmap="viridis")
    plt.title("Correlation matrix")
    _save_or_show(save_path)


def plot_mcg_by_region(df, save_path: str | None = None) -> None:
    """
    Plot lightning intensity by region using boxplots (may be slow on huge datasets).
    """
    plt.figure(figsize=(10, 5))
    sns.boxplot(x="region", y="mcg", data=df)
    plt.title("Lightning intensity (mcg) by region")
    plt.xlabel("Region")
    plt.ylabel("mcg")
    _save_or_show(save_path)


def plot_mcg_by_hour(df, save_path: str | None = None) -> None:
    """
    Plot lightning intensity by hour using boxplots (may be slow on huge datasets).
    """
    plt.figure(figsize=(12, 5))
    sns.boxplot(x="hour", y="mcg", data=df)
    plt.title("Lightning intensity (mcg) by hour")
    plt.xlabel("Hour")
    plt.ylabel("mcg")
    _save_or_show(save_path)