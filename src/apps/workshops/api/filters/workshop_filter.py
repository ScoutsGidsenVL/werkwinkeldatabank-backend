"""apps.workshops.api.filters.workshop_filter."""

import django_filters

from apps.base.filters import ActiveFilterMixin
from apps.filter_extensions.filters import MultipleUUIDFilter
from apps.workshops.models import Workshop
from apps.workshops.models.enums import WorkshopStatusType


class WorkshopFilter(ActiveFilterMixin, django_filters.FilterSet):
    term = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    theme = MultipleUUIDFilter(field_name="themes")
    duration_start = django_filters.DurationFilter(field_name="duration", lookup_expr="gte")
    duration_end = django_filters.DurationFilter(field_name="duration", lookup_expr="lte")
    is_sensitive = django_filters.BooleanFilter(method="is_sensitive_filter")
    status = django_filters.MultipleChoiceFilter(choices=WorkshopStatusType.choices, field_name="workshop_status_type")
    created_by = MultipleUUIDFilter()

    def is_sensitive_filter(self, queryset, name, value):  # pylint: disable=unused-argument
        if value:
            return queryset.filter(building_blocks__template__is_sensitive=True).distinct()
        return queryset.exclude(building_blocks__template__is_sensitive=True).distinct()

    class Meta:
        model = Workshop
        fields = []
