# src/main.py
from io_data import load_data, ensuoutput_dirs, export_clean_data
from cleaning import clean_and_types, add_time_features
from analysis import (
    print_basic_overview,
    print_uniques,
    print_time_range,
    correlation_matrix,
    top_correlations,
    linear_regression_mcg,
    print_regression_report,
)
from viz import (
    plot_strikes_per_region,
    plot_strikes_by_hour,
    plot_geo_intensity,
    plot_geo_intensity_map,  # NEU
    plot_intensity_hist,
    plot_corr_heatmap,
    plot_mcg_by_region,
    plot_mcg_by_hour,
)

def main():
    file_path = "resource/lightning_strikes.csv"

    ensuoutput_dirs("output")

    # 1) Load
    df_raw = load_data(file_path)
    print("\n--- RAW OVERVIEW ---")
    print_basic_overview(df_raw)

    # 2) Clean + Features
    df = clean_and_types(df_raw)
    df = add_time_features(df)

    print("\n--- AFTER CLEANING + FEATURES ---")
    print_basic_overview(df)
    print_time_range(df)
    print_uniques(df)
    print("\nHinweis: Jahre/Monate siehe Unique-Werte und Zeitraum-Ausgabe oben.")

    # 3) Analysis: Correlation
    corr = correlation_matrix(df)
    print("\n--- KORRELATIONSMATRIX ---")
    print(corr)

    print("\n--- TOP KORRELATIONEN MIT mcg (nach |corr|) ---")
    print(top_correlations(corr, target="mcg", n=5))

    # Export correlation matrix
    corr.to_csv("output/correlation_matrix.csv")
    print("\nKorrelationsmatrix exportiert nach: output/correlation_matrix.csv")

    # 3b) Analysis: Regression
    reg_result = linear_regression_mcg(df)
    print_regression_report(reg_result)

    # Export regression coefficients (if ok)
    if reg_result.get("ok"):
        reg_result["coefficients"].to_csv("output/regression_coefficients.csv")
        print("Regressions-Koeffizienten exportiert nach: output/regression_coefficients.csv")

    # 4) Visuals (anzeigen)
    plot_strikes_per_region(df)
    plot_strikes_by_hour(df)
    plot_geo_intensity(df)
    plot_geo_intensity_map(df)  # NEU: Basemap + Ländergrenzen
    plot_intensity_hist(df)
    plot_corr_heatmap(corr)

    # Zusätzliche Interpretationsplots
    plot_mcg_by_region(df)
    plot_mcg_by_hour(df)

    # 5) Export cleaned data
    export_clean_data(df, "output/lightning_strikes_clean.csv")

    # optional: Figuren speichern
    plot_strikes_per_region(df, "output/figures/region_bar.png")
    plot_strikes_by_hour(df, "output/figures/hour_line.png")
    plot_geo_intensity(df, "output/figures/geo_intensity.png")
    plot_geo_intensity_map(df, "output/figures/geo_intensity_map.png")  # NEU
    plot_intensity_hist(df, "output/figures/mcg_hist.png")
    plot_corr_heatmap(corr, "output/figures/corr_heatmap.png")
    plot_mcg_by_region(df, "output/figures/mcg_by_region_box.png")
    plot_mcg_by_hour(df, "output/figures/mcg_by_hour_box.png")

if __name__ == "__main__":
    main()