from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Publication, Comment


class PublicationAdmin(SummernoteModelAdmin):
    list_display = ('id', 'title', 'date_published', 'author',)
    list_filter = ('author', 'date_published')
    search_fields = ('author', 'date_published')
    empty_value_display = '-пусто-'
    summernote_fields = ('text',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'text',)


admin.site.register(Publication, PublicationAdmin)
admin.site.register(Comment, CommentAdmin)
