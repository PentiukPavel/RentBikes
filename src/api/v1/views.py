from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import (
    mixins,
    pagination,
    permissions,
    response,
    status,
    views,
    viewsets,
)

from api.v1.schemes import (
    BICYCLE_GET_EXAMPLE,
    BICYCLE_GET_200,
    BRAND_GET_EXAMPLE,
    BRAND_GET_200,
    USER_CREATE_EXAMPLE,
    USER_CREATED_201,
)
from api.v1.serializers import (
    BicycleSerializer,
    BrandGetSerializer,
    UserCreateSerializer,
)
from bicycles.models import Bicycle, Brand


@extend_schema(
    request=UserCreateSerializer,
    summary="Регистрация пользователя",
    tags=["Users"],
    examples=[USER_CREATE_EXAMPLE],
    responses={
        status.HTTP_201_CREATED: USER_CREATED_201,
    },
)
class RegisrtyView(views.APIView):
    """
    Регистрация пользователей.
    """

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return response.Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


@extend_schema(
    tags=["Bicycles"],
    examples=[BRAND_GET_EXAMPLE],
    responses={
        status.HTTP_200_OK: BRAND_GET_200,
    },
)
@extend_schema_view(
    list=extend_schema(summary="Список марок велосипедов"),
)
class BrandViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Марки велосипедов."""

    queryset = Brand.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BrandGetSerializer


@extend_schema(
    tags=["Bicycles"],
    examples=[BICYCLE_GET_EXAMPLE],
    responses={
        status.HTTP_200_OK: BICYCLE_GET_200,
    },
)
@extend_schema_view(
    list=extend_schema(summary="Список велосипедов"),
)
class BicycleViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Доступные Велосипеды."""

    serializer_class = BicycleSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Bicycle.cstm_mngr.filter(available=True)
