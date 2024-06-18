from django.contrib import admin

from distribution.models import Distribution, DistributionClient, Message


@admin.register(Distribution)
class DistributionAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'frequency', 'status', 'message')
    list_filter = ('status',)
    search_fields = ('frequency', 'status',)


@admin.register(DistributionClient)
class DistributionClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    list_filter = ('email', 'first_name')
    search_fields = ('email',)


@admin.register(Message)
class DistributionClientAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body')
    list_filter = ('subject',)
    search_fields = ('subject',)
