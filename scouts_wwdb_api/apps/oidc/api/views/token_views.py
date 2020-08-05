from rest_framework import APIView, status
from rest_framework.response import Response


class AuthCodeView(APIView):
    class InputSerializer(serializers.Serializer):
        authCode = serializers.CharField()
        clientId = serializers.CharField()
        realm = serializers.CharField()
        redirectUri = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tokens = get_tokens_by_auth_code(**serializer.validated_data)

        return Response()
