"""scouts_wwdb_api.urls.

scouts_wwdb_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import django
from django.urls import include, path

import drf_yasg.openapi
import drf_yasg.views
import rest_framework.permissions

# Open api schema
schema_view = drf_yasg.views.get_schema_view(
    drf_yasg.openapi.Info(
        title="Scouts WWDB API",
        default_version="v1",
        description="This is the api documentation for the Scouts WerkWinkelDataBank API",
    ),
    public=True,
    permission_classes=(rest_framework.permissions.AllowAny,),
)

urlpatterns = [
    path("api/", include("apps.workshops.urls")),
    path("api/auth/", include("apps.scouts_auth.urls")),
    path("api/oidc/", include("apps.oidc.urls")),
    path("api/files/", include("apps.files.urls")),
    path("admin/", django.contrib.admin.site.urls),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
