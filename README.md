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
    ├── analysis.py            # Analyse 
    ├── viz.py                 # Visualisierungen (Plots & Karten)
```

## Workflow / Pipeline

Das folgende Diagramm zeigt die komplette Datenpipeline dieses Projektes:
> Hinweis: Aufgrund der Größe des Workflows könnte das Diagramm im GitHub-Viewer standardmäßig minimiert dargestellt werden.  
> Über das Zoom-/Expand-Symbol lässt sich der vollständige Workflow anzeigen.

```mermaid
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

## KI-Deklaration

Im Rahmen dieses Projekts wurde Künstliche Intelligenz unterstützend und beratend eingesetzt.
Die Nutzung umfasste insbesondere:

	•	Beratung bei der Konzeption des Workflows und der Pipeline-Struktur
	•	Unterstützung bei der Formulierung von Code-Dokumentation
	•	Hilfestellung bei Fehlersuche, Codekorrektur und Refactoring
	•	Diskussion und Einordnung analytischer Schritte (z. B. Korrelationsanalyse)
