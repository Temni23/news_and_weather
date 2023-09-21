from django.contrib import admin
from django.utils.html import format_html

from .models import Publication


@admin.register(Publication)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_published', 'author',)
    list_filter = ('author', 'date_published')
    search_fields = ('author', 'date_published')
    empty_value_display = '-пусто-'

# TODO добавить поле с превью картинки в админку
