from django.db.models import Q


class SearchMixin:

    search_fields = []

    def apply_search_filter(self, queryset):

        query = self.request.GET.get('q')
        category_id = self.request.GET.get('category')

        if query and self.search_fields:
            search_query = Q()
            for field in self.search_fields:
                search_query |= Q(**{f'{field}__icontains': query})
            queryset = queryset.filter(search_query)

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset