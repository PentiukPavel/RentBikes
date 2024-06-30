import sys

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
from rest_framework.decorators import action

from api.v1.permissions import IsRenter
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
    RentGetSerializer,
    UserCreateSerializer,
)
from bicycles.models import Bicycle, Brand
from bicycles.services import rent_bike
from core.enums import APIResponces
from orders.models import Rent
from orders.tasks import calculate_rent_cost


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
    retrieve=extend_schema(summary="Информация о велосипеде"),
)
class BicycleViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """Доступные Велосипеды."""

    pagination_class = pagination.LimitOffsetPagination
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BicycleSerializer

    def get_queryset(self):
        return Bicycle.cstm_mngr.filter(available=True)

    @extend_schema(
        summary="Арендовать велосипед",
        methods=["POST"],
        request=None,
    )
    @action(
        detail=True,
        methods=("post",),
        url_path="rent",
        url_name="rent",
        permission_classes=(permissions.IsAuthenticated,),
    )
    def rent(self, request, *args, **kwargs):
        """Арендовать велосипед."""

        # проверяем есть ли у пользователя незавершенные аренды
        renter = self.request.user
        if Rent.cstm_mngr.filter(renter=renter, end_time=None).exists():
            return response.Response(
                data=APIResponces.UNFINISHED_RENTS_EXISTS.value,
                status=status.HTTP_423_LOCKED,
            )

        bicycle: Bicycle = self.get_object()
        rent_bike(bicycle, renter)
        serializer = self.get_serializer(bicycle)
        return response.Response(serializer.data)


@extend_schema(
    tags=["Rents"],
)
@extend_schema_view(
    list=extend_schema(summary="Список аренд пользователя"),
    retrieve=extend_schema(summary="Информация об аренде"),
)
class RentViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """Аренды."""

    permission_classes = (IsRenter,)
    serializer_class = RentGetSerializer

    def get_queryset(self):
        return Rent.cstm_mngr.filter(renter=self.request.user)

    @extend_schema(
        summary="Завершить аренду",
        methods=["POST"],
        request=None,
    )
    @action(
        detail=True,
        methods=("post",),
        url_path="complete",
        url_name="complete",
        permission_classes=[IsRenter],
    )
    def complete_this_rent(self, request, *args, **kwargs):
        """Завершить аренду."""

        rent: Rent = self.get_object()
        if rent.end_time is not None:
            return response.Response(
                data=APIResponces.RENT_ALREADY_COMPLETE.value,
                status=status.HTTP_423_LOCKED,
            )
        rent.complete_rent()
        if "test" not in sys.argv:
            calculate_rent_cost.delay(rent.id)
        else:
            rent.cost_calculation()
        serializer = self.get_serializer()
        return response.Response(serializer.data)
