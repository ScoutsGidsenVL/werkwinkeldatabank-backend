import django_filters
from ...models import Workshop


class WorkshopFilter(django_filters.FilterSet):
    term = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    theme = django_filters.UUIDFilter(lookup_expr="exact")

    class Meta:
        model = Workshop
        fields = []
