from django.urls import path, include

from PharmaQ.consultation.views.category_views import CategoryCreateView, CategoryEditView, CategoryDeleteView, \
    CategoryListView
from PharmaQ.consultation.views.question_views import QuestionCreateView, QuestionEditView, QuestionDeleteView, \
    QuestionListView

urlpatterns = [
    path('categories/', include([
        path('create/', CategoryCreateView.as_view(), name='category-create'),
        path('list/', CategoryListView.as_view(), name='category-list'),
        path('<str:slug>/', include([
            path('edit/', CategoryEditView.as_view(), name='category-edit'),
            path('delete/', CategoryDeleteView.as_view(), name='category-delete'),
        ]))
    ])),
    path('questions/', include([
        path('create/', QuestionCreateView.as_view(), name='question-create'),

        path('<int:pk>/', include([
            path('edit/', QuestionEditView.as_view(), name='question-edit'),
            path('delete/', QuestionDeleteView.as_view(), name='question-delete'),
            path('list/', QuestionListView.as_view(), name='question-list'),
        ]))
    ]))
]