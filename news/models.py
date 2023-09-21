import os
from PIL import Image

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Publication(models.Model):
    title = models.CharField(verbose_name='Заголовок новости',
                             max_length=255,
                             help_text='Введите небольшой заголовок новости')
    main_image = models.ImageField(verbose_name='Главное изображение',
                                   upload_to='news/images/',
                                   help_text='Добавьте изображение')
    preview_image = models.ImageField(upload_to='news/images/previews/',
                                      blank=True,
                                      editable=False)  # Превью-изображение (недоступное для редактирования)

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
                             200))  # Уменьшаем изображение до 200px по наименьшей стороне
            preview_image_path = os.path.join('media/news/images/previews/',
                                              os.path.basename(
                                                  self.main_image.name))
            image.save(preview_image_path)
            return preview_image_path
        return None

    def save(self, *args, **kwargs):
        if not self.preview_image:
            preview_image_path = self.generate_preview_image()
            if preview_image_path:
                self.preview_image.name = preview_image_path
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
