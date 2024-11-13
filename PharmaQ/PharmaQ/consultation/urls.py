from django.urls import path, include

from PharmaQ.consultation.views.category_views import CategoryCreateView, CategoryEditView, CategoryDeleteView, \
    CategoryListView

urlpatterns = [
    path('categories/', include([
        path('create/', CategoryCreateView.as_view(), name='category-create'),
        path('list/', CategoryListView.as_view(), name='category-list'),
        path('<str:slug>/', include([
            path('edit/', CategoryEditView.as_view(), name='category-edit'),
            path('delete/', CategoryDeleteView.as_view(), name='category-delete'),
        ]))
    ]))
]