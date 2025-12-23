import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# CSV file path
file_path = '../resource/lightning_strikes.csv'

# CSV-Datei einlesen:
data = pd.read_csv(
    file_path, 
    usecols=['time', 'lat', 'lon', 'region', 'mds', 'mcg', 'status']
)

# Überblick über die Daten
print(data.info())

print("\nDaten erfolgreich geladen.")

print(f"Der Datensatz enthält {data.shape[1]} Spalten und {data.shape[0]} Zeilen")

print("\nEs gibt 2 Spalten mit float Daten (lat, lon), 4 Spalten mit Objekt-Daten (time, region, mds, mcg, status) und keine fehlenden Werte.")

print("\nAnzahl der fehlenden Werte pro Spalte:")
null_werte_anzahl = data.isnull().sum()
print(null_werte_anzahl)

# Konvertierung der 'time'-Spalte
data['time'] = pd.to_datetime(data['time'], unit='ns')
# Extrahieren von Jahr, Monat, Stunde, Minute und Sekunde
data['year'] = data['time'].dt.year
data['month'] = data['time'].dt.month
data['hour'] = data['time'].dt.hour
data['minute'] = data['time'].dt.minute
data['second'] = data['time'].dt.second

# Die ersten Zeilen zur Überprüfung anzeigen
print("\nDie ersten fünf Zeilen des Datensatzes:")
print(data.head())

# Eindeutigen Werte in der 'region'-Spalte anzeigen
eindeutige_region = data['region'].unique()
print("\nDie eindeutigen Werte in der Region 'region' sind:")
print(eindeutige_region)

# Eindeutigen Werte in der 'year'-Spalte anzeigen
eindeutige_jahre = data['year'].unique()
print("\nDie eindeutigen Werte in der Spalte 'year' sind:")
print(eindeutige_jahre)

# Eindeutigen Werte in der 'month'-Spalte anzeigen
eindeutige_monate = data['month'].unique()
print("\nDie eindeutigen Werte in der Spalte 'month' sind:")
print(eindeutige_monate)

print("\nDie Daten beschränken sich auf das Jahre 2025 in den Monaten November und Dezember.")

#Datenvisualisierung und mögliche Interpretation

#Balkendiagramm der Häufigkeit der Blitze pro Region
plt.figure(figsize=(8, 5))
data['region'].value_counts().plot(kind='bar')
plt.title('Häufigkeit der Blitze pro Region')
plt.ylabel('Anzahl der Blitze')
plt.xlabel('Region')
plt.xticks(rotation=0)
plt.show()

#Liniendiagramm der Blitzeinschläge über den Tag (Stunden)
plt.figure(figsize=(10, 6))
data.groupby('hour').size().plot(kind='line', marker='o')
plt.title('Blitzeinschläge über den Tag (Stunden)')
plt.xlabel('Stunde des Tages')
plt.ylabel('Anzahl der Blitze')
plt.xticks(range(24))
plt.grid(True)
plt.show()

#Scatterplot der Blitzeinschläge nach Intensität (mcg)
plt.figure(figsize=(10, 8))
sns.scatterplot(
    x='lon', 
    y='lat', 
    data=data, 
    hue='mcg', # Farbe nach Intensität
    size='mcg', # Größe nach Intensität
    alpha=0.3, 
    palette='viridis'
)
plt.title('Geografische Verteilung der Blitzeinschläge nach Intensität (mcg)')
plt.xlabel('Längengrad (lon)')
plt.ylabel('Breitengrad (lat)')
plt.show()

#Histogramm der Blitzintensität (mcg)
plt.figure(figsize=(8, 5))
sns.histplot(data['mcg'], bins=50, kde=True)
plt.title('Verteilung der Blitzintensität (mcg)')
plt.xlabel('mcg Wert')
plt.ylabel('Häufigkeit')
plt.show()