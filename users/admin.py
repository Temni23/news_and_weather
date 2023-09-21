from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'role',
                    'first_name', 'last_name',)
    list_editable = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('email', 'username')
    search_fields = ('id', 'email', 'username', 'first_name', 'last_name')
    empty_value_display = '-пусто-'
