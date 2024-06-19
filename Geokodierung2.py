import urllib.parse
import requests
from pymongo import MongoClient, InsertOne
import concurrent.futures

# MongoDB-Verbindung herstellen
client = MongoClient('mongodb://localhost:27017/')
db = client['Bogestra']  # Name der Datenbank mit Adressen
collection = db['BogestraGrouped']  # Sammlung mit Adressen

# Neue MongoDB-Datenbank/Sammlung für die Geokodierungsantworten
geocoded_db = client['geocoded_db']
geocoded_collection = geocoded_db['geocoded_adressen']

adressen = list(collection.find())

# Funktion zur Geokodierung einer Adresse
def geocode_address(eintrag):
    try:
        adresse = eintrag['Adresse']
        params = urllib.parse.quote_plus(adresse)
        params = params.replace("+", "%20")
        
        url = 'https://geocoder.fbg-hsbo.de/geocoder/geocode/query-string?q='
        url = url + params
        
        geocoder = requests.get(url)
        if geocoder.status_code == 200:
            result = geocoder.json()
            
            # Den Originaleintrag mit den Geokodierungsdaten zusammenführen
            geocoded_entry = {
                "original_address_entry": eintrag,
                "geocoded_data": result
            }
            return geocoded_entry
    except KeyError:
        # Fehler abfangen und überspringen, wenn der Schlüssel 'Adresse' fehlt
        print("Eintrag übersprungen: 'Adresse' Schlüssel fehlt")
    except Exception as e:
        # Allgemeine Fehler abfangen
        print(f"Ein Fehler ist aufgetreten: {e}")
    return None

# Zähler für erfolgreich geokodierte Adressen
count = 0
batch_size = 10
geocoded_entries = []

# Parallelisierung der Geokodierungsanfragen
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    future_to_address = {executor.submit(geocode_address, eintrag): eintrag for eintrag in adressen}
    for future in concurrent.futures.as_completed(future_to_address):
        geocoded_entry = future.result()
        if geocoded_entry:
            geocoded_entries.append(geocoded_entry)
            count += 1
            print(f"Geokodierte Adressen: {count}")
            
            # Wenn die Batch-Größe erreicht ist, in die Datenbank schreiben
            if len(geocoded_entries) >= batch_size:
                requests = [InsertOne(entry) for entry in geocoded_entries]
                geocoded_collection.bulk_write(requests)
                geocoded_entries = []  # Batch zurücksetzen

# Alle verbleibenden Einträge einfügen
if geocoded_entries:
    requests = [InsertOne(entry) for entry in geocoded_entries]
    geocoded_collection.bulk_write(requests)

print(f"Geokodierung abgeschlossen: {count} Adressen erfolgreich geokodiert und in die neue MongoDB-Datenbank geschrieben.")
