from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from .mixins import ProductListMixin, ProductMixin
from .serializers import ProductDetailSerializer, ProductSerializer


class ProductListView(ProductListMixin, ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer


class ProductView(ProductMixin, RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductDetailSerializer
