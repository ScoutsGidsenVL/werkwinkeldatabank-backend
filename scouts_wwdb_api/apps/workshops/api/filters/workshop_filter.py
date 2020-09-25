import django_filters
from ...models import Workshop
from apps.filter_extensions.filters import MultipleUUIDFilter


class WorkshopFilter(django_filters.FilterSet):
    term = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    theme = MultipleUUIDFilter()
    # is_sensitive = django_filters.BooleanFilter(field_name="is_sensitive")

    class Meta:
        model = Workshop
        fields = []
