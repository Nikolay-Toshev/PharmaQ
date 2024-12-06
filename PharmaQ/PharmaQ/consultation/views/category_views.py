
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from PharmaQ.common.mixins import SearchMixin
from PharmaQ.consultation.forms import CategoryCreateForm, CategoryEditForm
from PharmaQ.consultation.models import Category

UserModel = get_user_model()

class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'consultations/category/category-create.html'
    success_url = reverse_lazy('category-list')

    def test_func(self):
        return self.request.user.groups.filter(name__exact='site-moderator').exists()


class CategoryEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    form_class = CategoryEditForm
    template_name = 'consultations/category/category-edit.html'
    success_url = reverse_lazy('category-list')

    def test_func(self):
        return self.request.user.groups.filter(name__exact='site-moderator').exists()


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'consultations/category/category-delete.html'
    success_url = reverse_lazy('category-list')

    def test_func(self):
        return self.request.user.groups.filter(name__exact='site-moderator').exists()


class CategoryListView(SearchMixin, ListView):
    model = Category
    template_name = 'consultations/category/category-list.html'
    context_object_name = 'categories'
    paginate_by = 10

    search_fields = ['title']

    def get_queryset(self):
        queryset =  Category.objects.all()
        queryset = self.apply_search_filter(queryset)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context