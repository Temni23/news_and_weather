from django.contrib.auth.models import AbstractUser
from django.db import models

from news_and_weather.settings import MAX_LENGTH_EMAIL, STR_SYMBOLS_AMOUNT


class User(AbstractUser):
    """Модель пользователя для проекта."""
    READER = 'reade'
    WRITER = 'writer'
    ADMIN = 'admin'

    ROLE_CHOICES = (
        (READER, 'Читатель'),
        (WRITER, 'Автор'),
        (ADMIN, 'Администратор'),
    )

    email = models.EmailField('Электронная почта',
                              max_length=MAX_LENGTH_EMAIL,
                              unique=True)
    role = models.CharField('Роль пользователя',
                            max_length=STR_SYMBOLS_AMOUNT,
                            choices=ROLE_CHOICES, default=READER)

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == User.ADMIN

    @property
    def is_reader(self):
        return self.role == User.READER

    @property
    def is_writer(self):
        return self.role == User.WRITER
