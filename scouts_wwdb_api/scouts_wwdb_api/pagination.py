"""scouts_wwdb_api.pagination."""
import rest_framework.pagination


class ScoutsPageNumberPagination(rest_framework.pagination.PageNumberPagination):
    page_size = 10
    max_page_size = 1000
    page_query_param = "page"
    page_size_query_param = "page_size"
