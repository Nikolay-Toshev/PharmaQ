from django.urls import path, include
from PharmaQ.consultation.views import CategoryCreateView, CategoryEditView, CategoryDeleteView, \
    CategoryListView, AnswerCreateView, AnswerListView, AnswerEditView, AnswerDeleteView, MyQuestionDetailView
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

        path('user/<int:user_pk>/question/<int:question_pk>/', include([
            path('edit/', QuestionEditView.as_view(), name='question-edit'),
            path('delete/', QuestionDeleteView.as_view(), name='question-delete'),
            path('details/', MyQuestionDetailView.as_view(), name='my-question-details'),
        ])),
        path('patient/<int:user_pk>/list/', MyQuestionsListView.as_view(), name='my-question-list'),
        path('pharmacist/<int:user_pk>/list/', UnansweredQuestionsListView.as_view(), name='unanswered-question-list'),
    ])),
    path('answers/', include([
        path('question/<int:question_pk>/create/', AnswerCreateView.as_view(), name='answer-create'),
        path('user/<int:user_pk>/', include([
            path('list/', AnswerListView.as_view(), name='answer-list'),
            path('answer/<int:answer_pk>/', include([
                path('edit/', AnswerEditView.as_view(), name='answer-edit'),
                path('delete/', AnswerDeleteView.as_view(), name='answer-delete'),
            ])),
        ]))
    ]))
]

