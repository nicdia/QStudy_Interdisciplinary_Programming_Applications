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