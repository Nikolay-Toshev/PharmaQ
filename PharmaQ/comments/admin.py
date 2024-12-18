from django.contrib import admin

from PharmaQ.comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ('author', 'content', 'answer', 'created_at', 'updated_at')

    search_fields = ('author__username', 'content', 'answer__content')

    fields = ('author', 'content', 'answer')