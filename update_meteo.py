import requests
import pandas as pd
from datetime import datetime, timedelta

# Configuration de l'API
API_KEY = 'd72efd6039d748830031be5f8d64c71d'
LOCATION = 'France'  # Vous pouvez spécifier une ville ou des coordonnées précises
URL = f'http://api.openweathermap.org/data/2.5/forecast?q={LOCATION}&exclude=current,minutely,daily,alerts&appid={API_KEY}&units=metric'

def fetch_weather_data():
    response = requests.get(URL)
    data = response.json()
    
    # Vérifier que la requête a réussi
    if response.status_code != 200:
        raise Exception(f"Erreur lors de la récupération des données météo: {data.get('message', '')}")
    
    # Extraire les prévisions (chaque 3 heures, donc 8 prévisions par jour)
    forecasts = data['list']
    
    # Créer une liste pour stocker les données
    weather_data = []
    
    for forecast in forecasts:
        time = datetime.fromtimestamp(forecast['dt'])
        temperature = forecast['main']['temp']
        weather_data.append({'time': time, 'temperature_2m (°C)': temperature})
    
    # Convertir en DataFrame
    df_weather = pd.DataFrame(weather_data)
    
    # Sauvegarder dans un fichier CSV
    df_weather.to_csv('meteo_previsions.csv', index=False)
    print("Données météo mises à jour avec succès.")

if __name__ == "__main__":
    fetch_weather_data()
