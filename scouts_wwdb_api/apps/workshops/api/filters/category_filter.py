import django_filters
from ...models import Category
from apps.base.filters import ActiveFilterMixin


class CategoryFilter(ActiveFilterMixin, django_filters.FilterSet):
    term = django_filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = Category
        fields = []
