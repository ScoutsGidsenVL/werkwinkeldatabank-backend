from rest_framework.views import APIView
from rest_framework import serializers
from ...models import Theme


class ThemeDetailApi(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Theme
            fields = ("id", "title")

    def get(self, request, theme_id):
        theme = Theme(title="test", description="This is a test")

        serializer = self.OutputSerializer(theme)

        return Response(serializer.data)
