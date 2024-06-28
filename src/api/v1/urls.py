from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.v1 import views

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"
    ),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("token/", TokenObtainPairView.as_view(), name="login"),
    path("registry/", views.RegisrtyView.as_view(), name="registry"),
]
