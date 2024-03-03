import logging

from requests.exceptions import HTTPError
from rest_framework import permissions, status, views
from rest_framework.response import Response

from apps.scouts_auth.inuits.logging import InuitsLogger
from ..exceptions import TokenRequestException
from ..services.token_request_service import get_tokens_by_auth_code, get_tokens_by_refresh_token
from .serializers import AuthCodeInputSerializer, RefreshInputSerializer, TokenOutputSerializer

logger: InuitsLogger = logging.getLogger(__name__)


class AuthCodeView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = AuthCodeInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        try:
            tokens = get_tokens_by_auth_code(auth_code=data.get("authCode"), redirect_uri=data.get("redirectUri"))
        except HTTPError as exc:
            logger.error("Failed to refresh tokens: {exc}")
            raise TokenRequestException("Failed to refresh tokens.")

        output_serializer = TokenOutputSerializer(tokens)

        return Response(output_serializer.data)


class RefreshView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RefreshInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        try:
            tokens = get_tokens_by_refresh_token(refresh_token=data.get("refreshToken"))
        except HTTPError as exc:
            logger.error("Failed to refresh tokens: {exc}")
            raise TokenRequestException("Failed to refresh tokens.")

        output_serializer = TokenOutputSerializer(tokens)

        return Response(output_serializer.data)
