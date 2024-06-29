from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

from api.v1 import views

v1_router = DefaultRouter()
v1_router.register("brands", views.BrandViewSet, basename="brands")
v1_router.register("bicycles", views.BicycleViewSet, basename="bicycles")
v1_router.register("rents", views.RentViewSet, basename="rents")

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"
    ),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("token/", TokenObtainPairView.as_view(), name="login"),
    path("registry/", views.RegisrtyView.as_view(), name="registry"),
    path("", include(v1_router.urls)),
]
