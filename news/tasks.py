from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from .custom_functions import get_emails
from .letter_constants import SUBJECT, MESSAGE, EMAIL_SENDER
from .models import Publication


@shared_task
def send_daily_news_email():
    """Отправляет рассылку с новостями за день."""
    today = timezone.now().date()
    subject = SUBJECT
    message = MESSAGE
    recipients = get_emails()
    email_sender = EMAIL_SENDER

    daily_news = Publication.objects.filter(date_published=today)

    news_list = "\n".join([f"- {news.title}" for news in daily_news])
    message += "\n\n" + news_list

    send_mail(subject, message, email_sender, recipients)
