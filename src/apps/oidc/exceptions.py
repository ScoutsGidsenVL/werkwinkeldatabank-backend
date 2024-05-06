"""apps.oidc.exceptions."""
from requests.exceptions import HTTPError
from rest_framework.exceptions import APIException


class TokenRequestException(APIException):
    status_code = 401
    default_detail = "Token request failed"
    default_code = "token_request_failed"

    def __init__(self, http_exception: HTTPError):
        detail = f"Token request failed with error: {http_exception} with message: {http_exception.response.text}"
        super().__init__(detail)
