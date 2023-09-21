from django.core.exceptions import ValidationError


def validate_coordinates(value):
    coordinates = value.split(',')

    if len(coordinates) != 2:
        raise ValidationError('Координаты должны содержать широту и долготу, '
                              'разделенные запятой.')

    latitude, longitude = coordinates
    try:
        latitude = float(latitude.strip())
        longitude = float(longitude.strip())
    except ValueError:
        raise ValidationError('Неверный формат координат. Введите числа.')

    if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
        raise ValidationError('Недопустимые значения для широты и долготы.')
