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