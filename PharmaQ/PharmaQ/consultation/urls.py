from django.urls import path, include

from PharmaQ.consultation.views import CategoryCreateView, CategoryEditView, CategoryDeleteView, \
    CategoryListView, AnswerCreateView, AnswerListView
from PharmaQ.consultation.views import QuestionCreateView, QuestionEditView, QuestionDeleteView, \
    MyQuestionsListView, UnansweredQuestionsListView

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
            path('list/', MyQuestionsListView.as_view(), name='question-list'),
            path('answer/', AnswerCreateView.as_view(), name='answer-create'),
        ])),
        path('list/', UnansweredQuestionsListView.as_view(), name='question-list-unanswered'),
    ])),
    path('answers/', include([
        path('pharmacist/<int:pk>/list/', AnswerListView.as_view(), name='answer-list'),
    ]))

]