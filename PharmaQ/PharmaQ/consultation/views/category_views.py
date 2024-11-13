
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from PharmaQ.consultation.forms import CategoryCreateForm, CategoryEditForm
from PharmaQ.consultation.models import Category

UserModel = get_user_model()

class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'consultations/category-create.html'
    success_url = reverse_lazy('category-list')

    def test_func(self):
        return self.request.user.groups.filter(name__exact='site-moderator').exists()


class CategoryEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    form_class = CategoryEditForm
    template_name = 'consultations/category-edit.html'
    success_url = reverse_lazy('category-list')

    def test_func(self):
        return self.request.user.groups.filter(name__exact='site-moderator').exists()


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'consultations/category-delete.html'
    success_url = reverse_lazy('category-list')

    def test_func(self):
        return self.request.user.groups.filter(name__exact='site-moderator').exists()


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'consultations/category-list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.all()
