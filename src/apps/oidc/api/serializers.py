"""apps.oidc.api.serializers."""

import rest_framework.serializers as drf_serializers


# These fields dont follow standard snake case python standard
# to keep oidc bundles consistent between django and symfony
class AuthCodeInputSerializer(drf_serializers.Serializer):
    authCode = drf_serializers.CharField()
    redirectUri = drf_serializers.CharField()


class RefreshInputSerializer(drf_serializers.Serializer):
    refreshToken = drf_serializers.CharField()


class TokenOutputSerializer(drf_serializers.Serializer):
    access_token = drf_serializers.CharField()
    refresh_token = drf_serializers.CharField()
