import django_filters
from django.db.models import Q
from ...models import BuildingBlockTemplate
from ...models.enums.building_block_type import BuildingBlockType


class BuildingBlockTemplateFilter(django_filters.FilterSet):
    term = django_filters.CharFilter(method="filter_by_term")
    type = django_filters.ChoiceFilter(choices=BuildingBlockType.choices, field_name="building_block_type")
    duration_start = django_filters.DurationFilter(field_name="duration", lookup_expr="gte")
    duration_end = django_filters.DurationFilter(field_name="duration", lookup_expr="lte")

    class Meta:
        model = BuildingBlockTemplate
        fields = []

    def filter_by_term(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(description__icontains=value))
