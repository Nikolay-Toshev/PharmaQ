from django.contrib import admin

from PharmaQ.consultation.models import Answer, Question, Category


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):

    list_display = ('creator_id', 'question_id', 'content', 'created_at', 'updated_at')

    search_fields = ('creator_id__username', 'content', )

    list_filter = ('question_id__category_id',)


    readonly_fields = ('created_at', 'updated_at')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    list_display = ('creator_id', 'title', 'category_id', 'content', 'created_at', 'updated_at')

    search_fields = ('creator_id__username', 'title', 'content')

    list_filter = ('category_id',)

    readonly_fields = ('created_at', 'updated_at', 'is_published')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('title', 'description')

    search_fields = ('title', 'description')

    readonly_fields = ('slug', )

