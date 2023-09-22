from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Publication
from constance import config

@shared_task
def send_daily_news_email():
    today = timezone.now().date()
    subject = config.email_subject
    message = config.email_message
    recipients = config.email_recipients

    daily_news = Publication.objects.filter(date_published=today)

    news_list = "\n".join([f"- {news.title}" for news in daily_news])
    message += "\n\n" + news_list

    send_mail(subject, message, config.email_sender, recipients)