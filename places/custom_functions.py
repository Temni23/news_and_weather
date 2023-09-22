import os
import requests

from dotenv import load_dotenv

from places.models import WeatherReport, Place
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")

load_dotenv()

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')

latitude = 51.51  # Широта
longitude = -0.13  # Долгота

url = f'http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={WEATHER_API_KEY}'
response = requests.get(url)
place = Place.objects.first()

if response.status_code == 200:
    weather_data = response.json()
    temperature = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    pressure = weather_data['main']['pressure']
    wind_speed = weather_data['wind']['speed']
    wind_direction = weather_data['wind']['deg']
    WeatherReport.objects.create(
        place=place,
        temperature=temperature,
        humidity=humidity,
        pressure=pressure,
        wind_speed=wind_speed,
        wind_direction=wind_direction
    )
else:
    print('Ошибка при запросе данных о погоде')
