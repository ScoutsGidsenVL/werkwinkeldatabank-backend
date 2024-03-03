import django_filters

from apps.base.filters import ActiveFilterMixin

from ...models import Theme


class ThemeFilter(ActiveFilterMixin, django_filters.FilterSet):
    term = django_filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = Theme
        fields = []
