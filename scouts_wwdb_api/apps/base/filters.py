import django_filters


class ActiveFilterMixin(django_filters.FilterSet):
    active = django_filters.BooleanFilter(method="active_filter")

    def active_filter(self, queryset, name, value):
        if value:
            return queryset.active()
        else:
            return queryset.inactive()
