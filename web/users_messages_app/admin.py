from django.contrib import admin
from .models import PrivateMessagesModel


class PrivateMessagesModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'recipient', 'timestamp', 'message']
    list_display_links = ['id']


admin.site.register(PrivateMessagesModel, PrivateMessagesModelAdmin)
