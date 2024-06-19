import urllib.parse
import requests
from pymongo import MongoClient, InsertOne
import concurrent.futures

# MongoDB-Verbindung herstellen
client = MongoClient('mongodb://localhost:27017/')
db = client['Bogestra']  # Name der Datenbank mit Adressen
collection = db['BogestraGrouped']  # Sammlung mit Adressen

# Neue MongoDB-Datenbank/Sammlung für die Geokodierungsantworten
geocoded_db = client['Bogestra']
geocoded_collection = geocoded_db['BogestraGeocoded']

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

# Hauptteil des Codes zur Verarbeitung der Adressen
def process_addresses():
    adressen = list(collection.find())
    
    # Zähler für erfolgreich geokodierte Adressen
    total_count = 0

    batch_size = 10000
    
    # Liste zum Sammeln der Geokodierungsdaten
    geocoded_entries = []
    
    # Parallelisierung der Geokodierungsanfragen
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_address = {executor.submit(geocode_address, eintrag): eintrag for eintrag in adressen}
        for future in concurrent.futures.as_completed(future_to_address):
            geocoded_entry = future.result()
            if geocoded_entry:
                geocoded_entries.append(geocoded_entry)
                total_count += 1
                print(f"Geokodierte Adressen: {total_count}")

                # Wenn die Batch-Größe erreicht ist, in die Datenbank schreiben
                if len(geocoded_entries) >= batch_size:
                    requests = [InsertOne(entry) for entry in geocoded_entries]
                    geocoded_collection.bulk_write(requests)
                    geocoded_entries = []  # Batch zurücksetzen
                    print("Geschrieben!!!")

    # Batch-Insert in die MongoDB-Sammlung
    if geocoded_entries:
        requests = [InsertOne(entry) for entry in geocoded_entries]
        geocoded_collection.bulk_write(requests)
    
    
    print(f"Geokodierung abgeschlossen: {total_count} Adressen erfolgreich geokodiert und in die neue MongoDB-Datenbank geschrieben.")

process_addresses()
