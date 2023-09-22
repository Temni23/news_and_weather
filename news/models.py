import os
from PIL import Image

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Publication(models.Model):
    """Модель для публикации новости."""
    title = models.CharField(verbose_name='Заголовок новости',
                             max_length=255,
                             help_text='Введите небольшой заголовок новости')
    main_image = models.ImageField(verbose_name='Главное изображение',
                                   upload_to='news/images/',
                                   help_text='Добавьте изображение')
    preview_image = models.ImageField(upload_to='news/images/previews/',
                                      blank=True,
                                      editable=False)

    text = models.TextField(verbose_name='Текст новости',
                            help_text='Введите текст новости')
    date_published = models.DateField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def generate_preview_image(self):
        if self.main_image:
            image = Image.open(self.main_image)
            image.thumbnail((200,
                             200))
            preview_image_path = os.path.join('media/news/images/previews/',
                                              os.path.basename(
                                                  self.main_image.name))
            image.save(preview_image_path)
            return preview_image_path
        return None

    def save(self, *args, **kwargs):
        preview_image_path = self.generate_preview_image()
        self.preview_image.name = preview_image_path
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Модель для комментария к новости."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    publication = models.ForeignKey(
        Publication, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']

    def __str__(self):
        return self.text
