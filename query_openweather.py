import requests

def get_weather(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric'  # oC
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error fetching weather data:", e)
        return None


if __name__ == "__main__":
    lat = 21.0285   
    lon = 105.8542
    api_key = "....."  

    weather_data = get_weather(lat, lon, api_key)
    if weather_data:
        print("Temperature", weather_data['main']['temp'], "°C")
        print("Weather", weather_data['weather'][0]['description'])
