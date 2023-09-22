import os
import requests

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_admin_geomap import GeoItem
from decimal import Decimal, ROUND_HALF_UP

from dotenv import load_dotenv

from news_and_weather.settings import (MIN_RATING, MAX_RATING,
                                       STR_SYMBOLS_AMOUNT, MAX_DIGITS,
                                       MAX_DECIMAL)

load_dotenv()

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')


class Place(models.Model, GeoItem):
    """Модель для примечательного места."""
    name = models.CharField(max_length=255, verbose_name='Название места',
                            unique=True)
    lon = models.FloatField(validators=[MinValueValidator(-180),
                                        MaxValueValidator(180)])
    lat = models.FloatField(validators=[MinValueValidator(-90),
                                        MaxValueValidator(90)])
    rating = models.DecimalField(
        max_digits=4, decimal_places=MAX_DECIMAL, verbose_name='Рейтинг',
        default=0,
        validators=[MinValueValidator(MIN_RATING),
                    MaxValueValidator(MAX_RATING)])

    class Meta:
        ordering = ['id']
        verbose_name = 'Место'
        verbose_name_plural = 'Места'

    def __str__(self):
        return self.name

    @property
    def geomap_longitude(self):
        return str(self.lon)

    @property
    def geomap_latitude(self):
        return str(self.lat)

    def get_weather(self):
        """Получает и сохраняет сводку о погоде для объекта."""
        url = (f'http://api.openweathermap.org/data/2.5/weather?lat='
               f'{self.lat}&lon={self.lon}&appid={WEATHER_API_KEY}')
        response = requests.get(url)

        try:
            response = requests.get(url)
            response.raise_for_status()

            weather_data = response.json()
            temperature = Decimal(weather_data['main']['temp']).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP)
            temperature_celsius = (
                (temperature - 273)).quantize(
                Decimal('0.00'), rounding=ROUND_HALF_UP)
            humidity = (Decimal(weather_data['main']['humidity']).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP))
            pressure = Decimal(weather_data['main']['pressure']).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP) * Decimal(
                0.75006375541921)
            wind_direction = weather_data['wind']['deg']
            wind_speed = Decimal(weather_data['wind']['speed']).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP)
            WeatherReport.objects.create(
                place=self,
                temperature=temperature_celsius,
                humidity=humidity,
                pressure=pressure,
                wind_speed=wind_speed,
                wind_direction=wind_direction
            )
        except requests.exceptions.RequestException as exception:
            raise Exception(f'Ошибка при запросе данных о погоде:'
                            f'{str(exception)}')


class WeatherReport(models.Model):
    """Модель для сводки с погодой."""
    place = models.ForeignKey(Place, on_delete=models.CASCADE,
                              related_name='weather_reports', editable=False)
    temperature = models.DecimalField(max_digits=MAX_DIGITS,
                                      decimal_places=MAX_DECIMAL,
                                      verbose_name='Температура (°C)',
                                      editable=False)
    humidity = models.DecimalField(max_digits=MAX_DIGITS,
                                   decimal_places=MAX_DECIMAL,
                                   verbose_name='Влажность (%)',
                                   editable=False)
    pressure = models.DecimalField(max_digits=MAX_DIGITS,
                                   decimal_places=MAX_DECIMAL,
                                   verbose_name='Атмосферное давление '
                                                '(мм рт. ст.)', editable=False)
    wind_direction = models.CharField(max_length=STR_SYMBOLS_AMOUNT,
                                      verbose_name='Направление ветра',
                                      editable=False)
    wind_speed = models.DecimalField(max_digits=MAX_DIGITS,
                                     decimal_places=MAX_DECIMAL,
                                     verbose_name='Скорость ветра (м/с)',
                                     editable=False)
    report_time = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Время сводки',
                                       editable=False)

    class Meta:
        verbose_name = 'Сводка погоды'
        verbose_name_plural = 'Сводки погоды'
        ordering = ['-report_time']

    def __str__(self):
        return f'Сводка погоды в {self.place} ({self.report_time})'
