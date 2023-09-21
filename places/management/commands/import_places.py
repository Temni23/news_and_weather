import os
import pandas as pd
from django.core.management.base import BaseCommand
from places.models import Place


class Command(BaseCommand):
    help = 'Импорт Примечательных мест из places.xlsx'

    def handle(self, *args, **kwargs):
        # Формируем полный путь к файлу данных
        base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(base_dir, '../import_data', 'places.xlsx')

        try:
            data_file = pd.read_excel(file_path)
            places_to_create = []

            for _, row in data_file.iterrows():
                name = row['name']
                lon = row['lon']
                lat = row['lat']
                rating = row['rating']

                place = Place(name=name, lon=lon, lat=lat, rating=rating)
                places_to_create.append(place)

            Place.objects.bulk_create(places_to_create)

            self.stdout.write(
                self.style.SUCCESS('Данные успешно импортированы'))
        except Exception as error:
            self.stderr.write(
                self.style.ERROR(f'Ошибка импорта данных: {str(error)}'))

