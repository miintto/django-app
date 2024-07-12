from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response

from .mixins import OrderMixin
from .serializers import OrderSerializer, OrderParamSerializer


class OrderView(OrderMixin, GenericAPIView):
    serializer_class = OrderSerializer

    def post(self, request):
        serializer = OrderParamSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        order.create_items(serializer.validated_data["items"])
        return Response(data=self.get_serializer(order).data, status=200)


class OrderSearchView(OrderMixin, RetrieveAPIView):
    serializer_class = OrderSerializer
