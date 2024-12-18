from django.urls import path, include
from PharmaQ.comments.views import CommentEditView, CommentDeleteView

urlpatterns = [
    path('<int:pk>/', include([
        path('edit/', CommentEditView.as_view(), name='comment-edit'),
        path('delete/', CommentDeleteView.as_view(), name='comment-delete'),
    ])),

]