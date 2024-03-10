"""apps.base.filters."""
import django_filters


class ActiveFilterMixin(django_filters.FilterSet):
    active = django_filters.BooleanFilter(method="active_filter")

    def active_filter(self, queryset, name, value):
        """Filter for active/inactive objects.
        
        The callable receives a QuerySet, 
        the name of the model field to filter on, 
        and the value to filter with. 
        It should return a filtered Queryset.
        """
        if value:
            return queryset.active()
        return queryset.inactive()
