"""apps.oidc.exceptions."""
import requests
import rest_framework.exceptions as drf_exceptions


class TokenRequestException(drf_exceptions.APIException):
    status_code = 401
    default_detail = "Token request failed"
    default_code = "token_request_failed"

    def __init__(self, http_exception: requests.exceptions.HTTPError):
        detail = f"Token request failed with error: {http_exception} with message: {http_exception.response.text}"
        super().__init__(detail)
