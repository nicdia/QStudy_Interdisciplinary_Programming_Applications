flowchart TD
    A([Start])

    subgraph SETUP["Setup & Datenimport"]
        B[Pfad & Flags setzen]
        C[Output-Verzeichnisse erstellen]
        D[Rohdaten aus CSV laden]
        E[RAW Overview ausgeben]
    end

    subgraph CLEANING["Datenbereinigung & Feature Engineering"]
        F[Daten bereinigen & Typen konvertieren]
        G[Zeitfeatures erzeugen]
        H[Overview nach Cleaning]
        I[Zeitbereich ausgeben]
        J[Zeitabdeckung berechnen]
        K[Eindeutige Werte prüfen]
    end

    subgraph ANALYSIS["Explorative Datenanalyse"]
        L[Korrelationsmatrix berechnen]
        M[Top-Korrelationen mit mcg]
        N[Korrelationsmatrix exportieren]
    end

    subgraph VIS["Visualisierung"]
        O{Plots anzeigen}
        O --> O1[Balkendiagramm: Anzahl Strikes pro Region]
        O --> O2[Liniendiagramm: Anzahl Strikes nach Stunde 0-23]
        O --> O3[Karte: Geo-Scatter lon/lat, Farbe = mcg, optional Sampling]
        O --> O4[Histogramm: Verteilung mcg, bins=50, KDE]
        O --> O5[Heatmap: Korrelationsmatrix]
        O --> O6[Boxplot: mcg-Verteilung nach Region]
    end

    P[Clean Dataset exportieren]
    Z([Ende])

    A --> B --> C --> D --> E
    E --> F --> G --> H --> I --> J --> K
    K --> L --> M --> N --> P
    P --> O --> Z