from django.contrib import admin

from PharmaQ.message.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'created_at', "is_read")

    search_fields = ('sender__username', 'receiver_username')

    list_filter = ('is_read',)

    readonly_fields = ('created_at', 'is_read')


