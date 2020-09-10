from rest_framework.exceptions import APIException


class InvalidWorkflowTransitionException(APIException):
    status_code = 400
    default_detail = "Invalid workflow transition"
    default_code = "bad_request"

    def __init__(self, from_msg: str, to_msg: str):
        detail = "Something went wrong with the workflow transition: not allowed to go from status %s to status %s" % (
            from_msg,
            to_msg,
        )
        return super().__init__(detail)
