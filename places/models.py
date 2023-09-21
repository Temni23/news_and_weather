from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_admin_geomap import GeoItem

from news_and_weather.settings import MIN_RATING, MAX_RATING


class Place(models.Model, GeoItem):
    name = models.CharField(max_length=255, verbose_name='Название места')
    lon = models.FloatField(validators=[MinValueValidator(-180),
                                        MaxValueValidator(180)])
    lat = models.FloatField(validators=[MinValueValidator(-90),
                                        MaxValueValidator(90)])
    # TODO В переменные
    rating = models.DecimalField(
        max_digits=4, decimal_places=2, verbose_name='Рейтинг', default=0,
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
