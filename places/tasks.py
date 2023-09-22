from celery import shared_task

from places.models import Place


@shared_task
def get_weather_summary_for_all_places():
    """Получить погоду для всех примечательных мест."""
    places = Place.objects.all()
    for place in places:
        place.get_weather()
