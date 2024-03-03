import django_filters
from django.db.models import Q

from apps.base.filters import ActiveFilterMixin
from apps.filter_extensions.filters import MultipleUUIDFilter

from ...models import BuildingBlockTemplate
from ...models.enums import BuildingBlockStatus, BuildingBlockType


class BuildingBlockTemplateFilter(ActiveFilterMixin, django_filters.FilterSet):
    term = django_filters.CharFilter(method="filter_by_term")
    type = django_filters.ChoiceFilter(choices=BuildingBlockType.choices, field_name="building_block_type")
    status = django_filters.MultipleChoiceFilter(choices=BuildingBlockStatus.choices, field_name="status")
    duration_start = django_filters.DurationFilter(field_name="duration", lookup_expr="gte")
    duration_end = django_filters.DurationFilter(field_name="duration", lookup_expr="lte")
    category = MultipleUUIDFilter()
    theme = MultipleUUIDFilter()
    created_by = MultipleUUIDFilter()

    class Meta:
        model = BuildingBlockTemplate
        fields = []

    def filter_by_term(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(description__icontains=value))
