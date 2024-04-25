import csv
import fileinput
import os
import sys

# Daten für die neue Zeile
neue_daten = ['Wert1', 'Wert2', 'Wert3', 'Wert4', 'Wert5', 'Wert6','Wert7', 'Wert8', 'Wert9','Wert10', 'Wert11', 'Wert12', 'Wert13', 'Wert14', 'Wert15', 'Wert16','Wert17', 'Wert18', 'Wert19','Wert20', 'Wert21', 'Wert22', 'Wert23', 'Wert24', 'Wert25', 'Wert26','Wert27', 'Wert28', 'Wert29','Wert30', 'Wert31', 'Wert32', 'Wert33', 'Wert34', 'Wert35', 'Wert36','Wert37', 'Wert38']
# Verzeichnis, in dem sich die CSV-Dateien befinden
verzeichnis = 'C:/Users/david/Documents/Trip_Requests/'

# Durchsuche das Verzeichnis nach CSV-Dateien
for datei_name in os.listdir(verzeichnis):
    if datei_name.endswith('.csv'):
        datei_pfad = os.path.join(verzeichnis, datei_name)
        print(datei_pfad)
        
        try:
            # Öffne die CSV-Datei und lese die vorhandenen Zeilen
            with open(datei_pfad, mode='r', newline='', encoding='latin-1') as file:
                reader = csv.reader(file, delimiter=';')
                zeilen = list(reader)
        except Exception as e:
            print(f"Fehler beim Lesen der Datei '{datei_pfad}': {e}")
            continue            

        # Füge die neue Zeile oben hinzu
        zeilen.insert(0, neue_daten)
        
        # Schreibe die Zeilen zurück in die Datei
        with open(datei_pfad, mode='w', newline='', encoding='latin-1') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(zeilen)
        
print("Neue Zeile erfolgreich zu allen CSV-Dateien hinzugefügt.")
