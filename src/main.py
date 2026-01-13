from io_data import load_data, ensure_output_dirs, export_clean_data
from cleaning import clean_and_types, add_time_features
from analysis import (
    print_basic_overview,
    print_uniques,
    print_time_range,
    print_time_granularity,
    correlation_matrix,
    top_correlations,
)
from viz import (
    plot_strikes_per_region,
    plot_strikes_by_hour,
    plot_geo_intensity_map,
    plot_intensity_hist,
    plot_corr_heatmap,
    plot_mcg_by_region,
)


def main() -> None:
    """
    Run the end-to-end pipeline: load, clean, feature engineer, analyze, visualize,
    and export results with sensible defaults for large datasets.
    """
    file_path = "resource/lightning_strikes.csv"

    # Toggle behavior
    SHOW_PLOTS = True
    SAVE_PLOTS = True

    ensure_output_dirs("output")

    df_raw = load_data(file_path)
    print("\n--- RAW OVERVIEW ---")
    print_basic_overview(df_raw)

    df = clean_and_types(df_raw)
    df = add_time_features(df)

    print("\n--- AFTER CLEANING + FEATURES ---")
    print_basic_overview(df)
    print_time_range(df)
    print_time_granularity(df)
    print_uniques(df)

    corr = correlation_matrix(df)
    print("\n--- CORRELATION MATRIX ---")
    print(corr)

    print("\n--- TOP CORRELATIONS WITH mcg (by |corr|) ---")
    print(top_correlations(corr, target="mcg", n=5))

    corr.to_csv("output/correlation_matrix.csv")
    print("\nExported correlation matrix to: output/correlation_matrix.csv")

    export_clean_data(df, "output/lightning_strikes_clean.csv")

    if SHOW_PLOTS:
        plot_strikes_per_region(df)
        plot_strikes_by_hour(df)
        plot_geo_intensity_map(df)
        plot_intensity_hist(df)
        plot_corr_heatmap(corr)
        plot_mcg_by_region(df)

    if SAVE_PLOTS:
        plot_strikes_per_region(df, "output/figures/region_bar.png")
        plot_strikes_by_hour(df, "output/figures/hour_line.png")
        plot_geo_intensity_map(df, "output/figures/geo_intensity_map.png")
        plot_intensity_hist(df, "output/figures/mcg_hist.png")
        plot_corr_heatmap(corr, "output/figures/corr_heatmap.png")
        plot_mcg_by_region(df, "output/figures/mcg_by_region_box.png")


if __name__ == "__main__":
    main()