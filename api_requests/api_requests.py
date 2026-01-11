import requests

city = "Paris"
api_key = "b7ddf049b61ab5914772ed900ccdc291"
api_url = f"http://api.weatherstack.com/current?access_key={api_key}&query={city}"

def fetch_weather_data():
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        raise

def mock_fetch_weather_data():
    return {'request': {'type': 'City', 'query': 'Paris, France', 'language': 'en', 'unit': 'm'}, 'location': {'name': 'Paris', 'country': 'France', 'region': 'Ile-de-France', 'lat': '48.867', 'lon': '2.333', 'timezone_id': 'Europe/Paris', 'localtime': '2026-01-09 09:22', 'localtime_epoch': 1767950520, 'utc_offset': '1.0'}, 'current': {'observation_time': '08:22 AM', 'temperature': 7, 'weather_code': 296, 'weather_icons': ['https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0017_cloudy_with_light_rain.png'], 'weather_descriptions': ['Light Drizzle'], 'astro': {'sunrise': '08:42 AM', 'sunset': '05:14 PM', 'moonrise': 'No moonrise', 'moonset': '11:32 AM', 'moon_phase': 'Waning Gibbous', 'moon_illumination': 66}, 'air_quality': {'co': '175.85', 'no2': '17.05', 'o3': '57', 'so2': '2.65', 'pm2_5': '4.15', 'pm10': '7.85', 'us-epa-index': '1', 'gb-defra-index': '1'}, 'wind_speed': 37, 'wind_degree': 254, 'wind_dir': 'WSW', 'pressure': 991, 'precip': 0.3, 'humidity': 76, 'cloudcover': 100, 'feelslike': 3, 'uv_index': 0, 'visibility': 10, 'is_day': 'yes'}}
