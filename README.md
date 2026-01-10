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
> Hinweis: Aufgrund der Größe des Workflows könnte das Diagramm im GitHub-Viewer standardmäßig minimiert dargestellt werden.  
> Über das Zoom-/Expand-Symbol lässt sich der vollständige Workflow anzeigen.

```mermaid
flowchart TD
    A([Start])

    subgraph SETUP["Setup & Datenimport"]
        B[Pfad- und Konfigurationseinstellungen]
        C[Ausgabeverzeichnisse erstellen]
        D[Rohdaten aus CSV laden]
        E[Überblick über Rohdaten]
    end

    subgraph CLEANING["Datenbereinigung & Feature Engineering"]
        F[Daten bereinigen und Typen konvertieren]
        G[Zeitbasierte Features erzeugen]
        H[Überblick nach Bereinigung]
        I[Zeitraum und zeitliche Abdeckung]
        J[Prüfung eindeutiger Werte]
    end

    subgraph ANALYSIS["Explorative Datenanalyse"]
        K[Korrelationsanalyse]
        L[Stärkste Korrelationen mit mcg]
        M[Korrelationsmatrix exportieren]
    end

    subgraph MODEL["Modellierung"]
        N[Lineares Regressionsmodell]
        O[Regressionsbericht]
        P{Regression erfolgreich?}
        Q[Regressionskoeffizienten exportieren]
        R[Export überspringen]
    end

    subgraph OUTPUT["Visualisierung & Export"]
        S[Bereinigten Datensatz exportieren]
        T{Plots anzeigen?}
        U[Plots erzeugen]
        V[Anzeige überspringen]
        W{Plots speichern?}
        X[Grafiken auf Festplatte speichern]
        Y[Speichern überspringen]
    end

    Z([Ende])

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
    P -- Ja --> Q
    P -- Nein --> R
    Q --> S
    R --> S
    S --> T
    T -- Ja --> U
    T -- Nein --> V
    U --> W
    V --> W
    W -- Ja --> X
    W -- Nein --> Y
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

