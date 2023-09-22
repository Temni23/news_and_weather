"""
Здесь хранятся переменные для
"""
import os
from constance import config

from dotenv import load_dotenv

load_dotenv()

SUBJECT = config.SUBJECT
MESSAGE = config.MESSAGE
EMAIL_SENDER = os.getenv('EMAIL_SENDER')