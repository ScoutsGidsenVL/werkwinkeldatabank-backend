"""apps.filter_extensions.fields"""
import django_filters


class BaseQueryArrayField(django_filters.fields.BaseCSVField):
    """an extension of BaseCSVField that uses QueryArrayWidget instead of csv widget"""

    base_widget_class = django_filters.widgets.QueryArrayWidget
