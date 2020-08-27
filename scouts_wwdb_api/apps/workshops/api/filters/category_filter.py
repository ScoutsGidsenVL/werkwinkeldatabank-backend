import django_filters
from ...models import Category


class CategoryFilter(django_filters.FilterSet):
    term = django_filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = Category
        fields = []
