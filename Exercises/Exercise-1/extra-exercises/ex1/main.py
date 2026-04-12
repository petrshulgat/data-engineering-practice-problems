import requests
import json
from pathlib import Path 

cities = [
    {"name": "Budapest", "lat": 47.4979, "lon": 19.0402},
    {"name": "London",   "lat": 51.5074, "lon": -0.1278},
    {"name": "New York", "lat": 40.7128, "lon": -74.0060},
    {"name": "Tokyo",    "lat": 35.6762, "lon": 139.6503},
    {"name": "Sydney",   "lat": -33.8688, "lon": 151.2093},
]

#https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true

def main():

    dir_name = Path('weather_data')
    dir_name.mkdir(exist_ok=True)

    for city in cities:

        url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={city['lat']}&longitude={city['lon']}&current_weather=true"
        )

        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        weather = data['current_weather']

        extracted = {
            'city' : city['name'],
            'temperature' : weather['temperature'],
            'windspeed' : weather['windspeed'],
            'time' : weather['time']
        }

        filename = city['name'].lower().replace(' ', '_') + '.json'
        file_path = Path('weather_data') / filename

        with open(file_path, 'w') as f:
            json.dump(extracted, f)

        print(f"Saved {filename}")


if __name__ == '__main__':
    main()