import pandas as pd
import os

# Verzeichnis, in dem sich die CSV-Dateien befinden
verzeichnis_pfad = '/pfad/zum/verzeichnis'

# Liste, um alle DataFrames aus den CSV-Dateien zu speichern
alle_dfs = []

# Durch das Verzeichnis iterieren
for datei in os.listdir(verzeichnis_pfad):
    if datei.endswith('.csv'):
        # Den Pfad zur aktuellen Datei erstellen
        datei_pfad = os.path.join(verzeichnis_pfad, datei)
        # CSV-Datei in ein DataFrame einlesen und zur Liste hinzufügen
        df = pd.read_csv(datei_pfad)
        alle_dfs.append(df)

# Alle DataFrames in der Liste zu einer Tabelle zusammenführen
gesamt_tabelle = pd.concat(alle_dfs, ignore_index=True)

# Die gesamte Tabelle anzeigen
print(gesamt_tabelle)