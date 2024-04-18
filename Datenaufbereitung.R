rm(list = ls())
#install.packages("readr")
library(readr)
library(dplyr)

# Verzeichnis, in dem sich die CSV-Dateien befinden
verzeichnis_pfad <- "C:/Users/david/Documents/Trip_Requests"

# Liste, um alle DataFrames aus den CSV-Dateien zu speichern
alle_dfs <- list()

# Durch das Verzeichnis iterieren
dateien <- list.files(path = verzeichnis_pfad, pattern = "\\.csv$", full.names = TRUE)
for (datei in dateien) {
  # CSV-Datei in ein DataFrame einlesen und zur Liste hinzufügen
  df <- read_csv2(datei)
  alle_dfs[[datei]] <- df
}

# Alle DataFrames in der Liste zu einer Tabelle zusammenführen
gesamt_tabelle <- bind_rows(alle_dfs)

# Die gesamte Tabelle anzeigen
print(gesamt_tabelle)
