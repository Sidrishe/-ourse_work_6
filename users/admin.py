from django.contrib import admin

from users.models import User


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'avatar', 'comment',)
    list_filter = ('email',)
    search_fields = ('first_name', 'last_name', 'email',)
