# QStudy Interdisciplinary Programming Applications

Dieses Projekt verarbeitet und analysiert Blitzeinschlagsdaten mit einem
End-to-End-Workflow: Datenimport, Bereinigung, Feature Engineering, Analyse,
Visualisierung und Export der Ergebnisse.

## Projektstruktur

```
.
├── documentation/
│   └── workflow_markdown.md   # Workflow-/Projektnotizen
├── resource/
│   ├── Info.txt               # Spaltenbeschreibung der Daten
│   └── lightning_strikes.csv  # Eingabedaten (muss manuell hinzugefügt werden)
└── src/
    ├── main.py                # Einstiegspunkt: gesamter Pipeline-Run
    ├── io_data.py             # Datenimport/-export
    ├── cleaning.py            # Datenbereinigung
    ├── analysis.py            # Analyse + lineare Regression
    ├── viz.py                 # Visualisierungen (Plots & Karten)
```

## Workflow / Pipeline

The following diagram illustrates the complete end-to-end data pipeline implemented in this project.
> Hinweis: Aufgrund der Größe des Workflows kann das Diagramm im GitHub-Viewer standardmäßig minimiert dargestellt werden.  
> Über das Zoom-/Expand-Symbol lässt sich der vollständige Workflow anzeigen.

```mermaid
flowchart TD
    A([Start])

    subgraph SETUP["Setup & Loading"]
        B[Set paths and flags]
        C[Ensure output directories]
        D[Load raw CSV data]
        E[Raw data overview]
    end

    subgraph CLEANING["Cleaning & Feature Engineering"]
        F[Clean and convert types]
        G[Add time features]
        H[Post-clean overview]
        I[Time range and coverage]
        J[Unique values check]
    end

    subgraph ANALYSIS["Exploratory Data Analysis"]
        K[Correlation analysis]
        L[Top correlations for mcg]
        M[Export correlation matrix]
    end

    subgraph MODEL["Modeling"]
        N[Linear regression model]
        O[Regression report]
        P{Regression successful}
        Q[Export regression coefficients]
        R[Skip coefficient export]
    end

    subgraph OUTPUT["Visualization & Export"]
        S[Export cleaned dataset]
        T{Show plots}
        U[Generate plots]
        V[Skip showing plots]
        W{Save plots}
        X[Save figures to disk]
        Y[Skip saving plots]
    end

    Z([End])

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
    I --> J
    J --> K
    K --> L
    L --> M
    M --> N
    N --> O
    O --> P
    P -- Yes --> Q
    P -- No --> R
    Q --> S
    R --> S
    S --> T
    T -- Yes --> U
    T -- No --> V
    U --> W
    V --> W
    W -- Yes --> X
    W -- No --> Y
    X --> Z
    Y --> Z
```

## Datenquelle

Die Pipeline erwartet eine CSV-Datei unter `resource/lightning_strikes.csv`. Die
Spaltenbeschreibung befindet sich in `resource/Info.txt`.

## Voraussetzungen

Python 3.10+ wird empfohlen. Benötigte Bibliotheken:

- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn
- cartopy

Installationsbeispiel:

```
pip install pandas numpy scikit-learn matplotlib seaborn cartopy
```

## Ausführung

Vom Repository-Root:

```
python src/main.py
```

Der Standardlauf:

- lädt die CSV-Datei,
- bereinigt/standardisiert die Spalten,
- erzeugt Zeitfeatures,
- führt Korrelationen und eine lineare Regression durch,
- exportiert bereinigte Daten sowie Analyse-Ergebnisse,
- speichert Visualisierungen in `output/figures/` (konfigurierbar in `main.py`).

## Output

Beim Standardlauf werden u. a. erzeugt:

- `output/lightning_strikes_clean.csv`
- `output/correlation_matrix.csv`
- `output/regression_coefficients.csv`
- `output/figures/*.png`

## Hinweise zur Nutzung

- Für große Datensätze sind Stichproben in den Kartenplots aktiv (siehe `viz.py`).
- Falls Visualisierungen interaktiv angezeigt werden sollen, setze `SHOW_PLOTS = True`
  in `src/main.py`.