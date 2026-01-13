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
        O --> O1[Balkendiagramm: Blitzeinschläge pro Region]
        O --> O2[Liniendiagramm: Blitzeinschläge nach Tagesstunde]
        O --> O3[Karte: Geografische Verteilung der Blitze]
        O --> O4[Histogramm: Verteilung der Blitzintensität mcg]
        O --> O5[Heatmap: Korrelationsmatrix]
        O --> O6[Boxplot: Blitzintensität mcg nach Region]
    end

    P[Clean Dataset exportieren]
    Z([Ende])

    A --> B --> C --> D --> E
    E --> F --> G --> H --> I --> J --> K
    K --> L --> M --> N --> P
    P --> O --> Z