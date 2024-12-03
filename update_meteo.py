import requests
import pandas as pd
from datetime import datetime, timedelta
import os

# Configuration de l'API Open-Meteo
LATITUDE = 48.8566  # Latitude de Paris
LONGITUDE = 2.3522   # Longitude de Paris
URL = f'https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&hourly=temperature_2m&forecast_days=3&timezone=Europe/Paris'

def fetch_weather_data():
    response = requests.get(URL)
    data = response.json()
    
    # Vérifier que la requête a réussi
    if response.status_code != 200:
        raise Exception(f"Erreur lors de la récupération des données météo: {data.get('reason', 'Unknown error')}")
    
    # Extraire les prévisions horaires (72 heures)
    hourly = data.get('hourly', {})
    times = hourly.get('time', [])
    temperatures = hourly.get('temperature_2m', [])
    
    if not times or not temperatures:
        raise Exception("Pas de données horaires trouvées dans la réponse de l'API.")
    
    # Limiter aux prochaines 72 heures
    current_time = datetime.now()
    cutoff_time = current_time + timedelta(hours=72)
    
    weather_data = []
    for time_str, temp in zip(times, temperatures):
        time = datetime.fromisoformat(time_str)
        if time > cutoff_time:
            break
        weather_data.append({'time': time, 'temperature_2m (°C)': temp})
    
    # Convertir en DataFrame
    df_weather = pd.DataFrame(weather_data)
    
    # Sauvegarder dans un fichier CSV
    df_weather.to_csv('meteo_previsions.csv', index=False)
    print("Données météo mises à jour avec succès.")

if __name__ == "__main__":
    fetch_weather_data()

