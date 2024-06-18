from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'content', 'image', 'creation_date', 'publication_feature')
    list_filter = ('title', 'creation_date', 'publication_feature')
    search_fields = ('title', 'creation_date',)
