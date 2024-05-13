"""apps.oidc.api.views."""

import logging

from requests.exceptions import HTTPError
from rest_framework import permissions, views
from rest_framework.response import Response

from apps.oidc.api.serializers import AuthCodeInputSerializer, RefreshInputSerializer, TokenOutputSerializer
from apps.oidc.exceptions import TokenRequestException
from apps.oidc.services.token_request_service import get_tokens_by_auth_code, get_tokens_by_refresh_token

logger = logging.getLogger(__name__)


class AuthCodeView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = AuthCodeInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        try:
            tokens = get_tokens_by_auth_code(auth_code=data.get("authCode"), redirect_uri=data.get("redirectUri"))
        except HTTPError as exc:
            logger.error(f"Failed to refresh tokens: {exc}")
            raise TokenRequestException("Failed to refresh tokens.") from exc

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
            logger.error(f"Failed to refresh tokens: {exc}")
            raise TokenRequestException("Failed to refresh tokens.") from exc

        output_serializer = TokenOutputSerializer(tokens)
        return Response(output_serializer.data)
