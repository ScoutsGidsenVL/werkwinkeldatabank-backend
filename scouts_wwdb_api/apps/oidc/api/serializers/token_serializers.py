from rest_framework import serializers


# These fields dont follow standard snake case python standard to keep oidc bundles consistent
# between django and symfony
class AuthCodeInputSerializer(serializers.Serializer):
    authCode = serializers.CharField()
    clientId = serializers.CharField()
    realm = serializers.CharField()
    redirectUri = serializers.CharField()


class RefreshInputSerializer(serializers.Serializer):
    refreshToken = serializers.CharField()
    clientId = serializers.CharField()
    realm = serializers.CharField()
