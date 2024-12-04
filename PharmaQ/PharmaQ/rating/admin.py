from django.contrib import admin

from PharmaQ.rating.models import Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):

    list_display = ('patient_id', 'answer_id', 'like', 'dislike')

    list_filter = ('like', 'dislike')

    search_fields = ('patient_id__username', 'answer_id__content')

