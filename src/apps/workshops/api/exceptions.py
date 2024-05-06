from rest_framework.exceptions import APIException

from ..exceptions import InvalidWorkflowTransitionException


class InvalidWorkflowTransitionAPIException(APIException):
    status_code = 400
    default_detail = "Invalid workflow transition"
    default_code = "bad_request"

    def __init__(self, exception: InvalidWorkflowTransitionException):
        detail = str(exception)
        return super().__init__(detail)
