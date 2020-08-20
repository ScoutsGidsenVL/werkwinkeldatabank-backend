import django_filters
from ...models import Theme


class ThemeFilter(django_filters.FilterSet):
    term = django_filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = Theme
        fields = []
